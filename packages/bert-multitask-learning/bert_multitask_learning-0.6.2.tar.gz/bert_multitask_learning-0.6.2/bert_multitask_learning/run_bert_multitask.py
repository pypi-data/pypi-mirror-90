import argparse
import os
import time
from typing import Dict, Callable
from shutil import copytree, ignore_patterns, rmtree

import tensorflow as tf
from tensorflow.python.framework.errors_impl import NotFoundError as TFNotFoundError

from .input_fn import predict_input_fn, train_eval_input_fn
from .model_fn import BertMultiTask
from .params import DynamicBatchSizeParams, BaseParams
from .special_tokens import EVAL

# Fix duplicate log
LOGGER = tf.get_logger()
LOGGER.propagate = False


def create_keras_model(
        mirrored_strategy: tf.distribute.MirroredStrategy,
        params: BaseParams,
        mode='train',
        inputs_to_build_model=None,
        model=None):
    """init model in various mode

    train: model will be loaded from huggingface
    resume: model will be loaded from params.ckpt_dir, if params.ckpt_dir dose not contain valid checkpoint, then load from huggingface
    transfer: model will be loaded from params.init_checkpoint, the correspongding path should contain checkpoints saved using bert-multitask-learning
    predict: model will be loaded from params.ckpt_dir except optimizers' states
    eval: model will be loaded from params.ckpt_dir except optimizers' states, model will be compiled

    Args:
        mirrored_strategy (tf.distribute.MirroredStrategy): mirrored strategy
        params (BaseParams): params
        mode (str, optional): Mode, see above explaination. Defaults to 'train'.
        inputs_to_build_model (Dict, optional): A batch of data. Defaults to None.
        model (Model, optional): Keras model. Defaults to None.

    Returns:
        model: loaded model
    """
    with mirrored_strategy.scope():
        if model is None:
            model = BertMultiTask(params)
            # model.run_eagerly = True
        if mode == 'resume':
            model.compile()
            # build training graph
            # model.train_step(inputs_to_build_model)
            _ = model(inputs_to_build_model,
                      mode=tf.estimator.ModeKeys.PREDICT)
            # load ALL vars including optimizers' states
            try:
                model.load_weights(os.path.join(
                    params.ckpt_dir, 'model'), skip_mismatch=False)
            except TFNotFoundError:
                LOGGER.warn('Not resuming since no mathcing ckpt found')
        elif mode == 'transfer':
            # build graph without optimizers' states
            # calling compile again should reset optimizers' states but we're playing safe here
            _ = model(inputs_to_build_model,
                      mode=tf.estimator.ModeKeys.PREDICT)
            # load weights without loading optimizers' vars
            model.load_weights(os.path.join(params.init_checkpoint, 'model'))
            # compile again
            model.compile()
        elif mode == 'predict':
            _ = model(inputs_to_build_model,
                      mode=tf.estimator.ModeKeys.PREDICT)
            # load weights without loading optimizers' vars
            model.load_weights(os.path.join(params.ckpt_dir, 'model'))
        elif mode == 'eval':
            _ = model(inputs_to_build_model,
                      mode=tf.estimator.ModeKeys.PREDICT)
            # load weights without loading optimizers' vars
            model.load_weights(os.path.join(params.ckpt_dir, 'model'))
            model.compile()
        else:
            model.compile()
    return model


def _train_bert_multitask_keras_model(train_dataset: tf.data.Dataset,
                                      eval_dataset: tf.data.Dataset,
                                      model: tf.keras.Model,
                                      params: BaseParams,
                                      mirrored_strategy: tf.distribute.MirroredStrategy = None):
    # can't save whole model with model subclassing api due to tf bug
    # see: https://github.com/tensorflow/tensorflow/issues/42741
    # https://github.com/tensorflow/tensorflow/issues/40366
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=os.path.join(params.ckpt_dir, 'model'),
        save_weights_only=True,
        monitor='val_mean_acc',
        mode='auto',
        save_best_only=False)

    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=params.ckpt_dir)

    with mirrored_strategy.scope():
        model.fit(
            x=train_dataset,
            validation_data=eval_dataset,
            epochs=params.train_epoch,
            callbacks=[model_checkpoint_callback, tensorboard_callback],
            steps_per_epoch=params.train_steps_per_epoch
        )
    model.summary()


def train_bert_multitask(
        problem='weibo_ner',
        num_gpus=1,
        num_epochs=10,
        model_dir='',
        params: BaseParams = None,
        problem_type_dict: Dict[str, str] = None,
        processing_fn_dict: Dict[str, Callable] = None,
        model: tf.keras.Model = None,
        create_tf_record_only=False,
        steps_per_epoch=None,
        warmup_ratio=0.1,
        continue_training=False):
    """Train Multi-task Bert model

    About problem:
        There are two types of chaining operations can be used to chain problems.
            - `&`. If two problems have the same inputs, they can be chained using `&`.
                Problems chained by `&` will be trained at the same time.
            - `|`. If two problems don't have the same inputs, they need to be chained using `|`.
                Problems chained by `|` will be sampled to train at every instance.

        For example, `cws|NER|weibo_ner&weibo_cws`, one problem will be sampled at each turn, say `weibo_ner&weibo_cws`, then `weibo_ner` and `weibo_cws` will trained for this turn together. Therefore, in a particular batch, some tasks might not be sampled, and their loss could be 0 in this batch.

    About problem_type_dict and processing_fn_dict:
        If the problem is not predefined, you need to tell the model what's the new problem's problem_type
        and preprocessing function.
            For example, a new problem: fake_classification
            problem_type_dict = {'fake_classification': 'cls'}
            processing_fn_dict = {'fake_classification': lambda: return ...}

        Available problem type:
            cls: Classification
            seq_tag: Sequence Labeling
            seq2seq_tag: Sequence to Sequence tag problem
            seq2seq_text: Sequence to Sequence text generation problem

        Preprocessing function example:
        Please refer to https://github.com/JayYip/bert-multitask-learning/blob/master/README.md

    Keyword Arguments:
        problem {str} -- Problems to train (default: {'weibo_ner'})
        num_gpus {int} -- Number of GPU to use (default: {1})
        num_epochs {int} -- Number of epochs to train (default: {10})
        model_dir {str} -- model dir (default: {''})
        params {BaseParams} -- Params to define training and models (default: {DynamicBatchSizeParams()})
        problem_type_dict {dict} -- Key: problem name, value: problem type (default: {{}})
        processing_fn_dict {dict} -- Key: problem name, value: problem data preprocessing fn (default: {{}})
    """
    params.train_epoch = num_epochs
    params = get_params_ready(problem, num_gpus, model_dir,
                              params, problem_type_dict, processing_fn_dict)

    train_dataset = train_eval_input_fn(params)
    eval_dataset = train_eval_input_fn(params, mode=EVAL)
    if create_tf_record_only:
        return

    # get train_steps and update params
    if steps_per_epoch is not None:
        train_steps = steps_per_epoch
    else:
        train_steps = 0
        for _ in train_dataset:
            train_steps += 1
    params.update_train_steps(train_steps, warmup_ratio=warmup_ratio)

    train_dataset = train_dataset.repeat(params.train_epoch)

    one_batch = next(train_dataset.as_numpy_iterator())

    mirrored_strategy = tf.distribute.MirroredStrategy()

    if num_gpus > 1:
        train_dataset = mirrored_strategy.experimental_distribute_dataset(
            train_dataset)
        eval_dataset = mirrored_strategy.experimental_distribute_dataset(
            eval_dataset)

    # restore priority: self > transfer > huggingface
    if continue_training and tf.train.latest_checkpoint(params.ckpt_dir):
        mode = 'resume'
    elif tf.train.latest_checkpoint(params.init_checkpoint):
        mode = 'transfer'
    else:
        mode = 'train'

    model = create_keras_model(
        mirrored_strategy=mirrored_strategy, params=params, mode=mode, inputs_to_build_model=one_batch)

    _train_bert_multitask_keras_model(
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        model=model,
        params=params,
        mirrored_strategy=mirrored_strategy
    )
    return model


def get_params_ready(problem, num_gpus, model_dir, params, problem_type_dict, processing_fn_dict, mode='train', json_path=''):
    if params is None:
        params = DynamicBatchSizeParams()
    if not os.path.exists('models'):
        os.mkdir('models')
    if model_dir:
        base_dir, dir_name = os.path.split(model_dir)
    else:
        base_dir, dir_name = None, None
    # add new problem to params if problem_type_dict and processing_fn_dict provided
    if problem_type_dict:
        params.add_multiple_problems(
            problem_type_dict=problem_type_dict, processing_fn_dict=processing_fn_dict)
    params.assign_problem(problem, gpu=int(num_gpus),
                          base_dir=base_dir, dir_name=dir_name)
    if mode == 'train':
        params.to_json()
    else:
        params.from_json(json_path)
    return params


def trim_checkpoint_for_prediction(problem: str,
                                   input_dir: str,
                                   output_dir: str,
                                   problem_type_dict: Dict[str, str] = None,
                                   overwrite=True,
                                   fake_input_list=None):
    """Minimize checkpoint size for prediction.

    Since the original checkpoint contains optimizer's variable,
        for instance, if the use adam, the checkpoint size will 
        be three times of the size of model weights. This function 
        will remove those unused variables in prediction to save space.

    Note: if the model is a multimodal model, you have to provide fake_input_list that
        mimic the structure of real input.

    Args:
        problem (str): problem
        input_dir (str): input dir
        output_dir (str): output dir
        problem_type_dict (Dict[str, str], optional): problem type dict. Defaults to None.
        fake_input_list (List): fake input list to create dummy dataset
    """
    if overwrite and os.path.exists(output_dir):
        rmtree(output_dir)
    copytree(input_dir, output_dir, ignore=ignore_patterns(
        'checkpoint', '*.index', '*.data-000*'))
    base_dir, dir_name = os.path.split(output_dir)
    params = DynamicBatchSizeParams()
    params.add_multiple_problems(problem_type_dict=problem_type_dict)
    params.from_json(os.path.join(input_dir, 'params.json'))
    params.assign_problem(problem, base_dir=base_dir,
                          dir_name=dir_name, predicting=True)

    model = BertMultiTask(params)
    if fake_input_list is None:
        dummy_dataset = predict_input_fn(['fake']*5, params)
    else:
        dummy_dataset = predict_input_fn(fake_input_list*5, params)
    _ = model(next(dummy_dataset.as_numpy_iterator()),
              mode=tf.estimator.ModeKeys.PREDICT)
    model.load_weights(os.path.join(input_dir, 'model'))
    model.save_weights(os.path.join(params.ckpt_dir, 'model'))
    params.to_json()


def eval_bert_multitask(
        problem='weibo_ner',
        num_gpus=1,
        model_dir='',
        params=None,
        problem_type_dict=None,
        processing_fn_dict=None,
        model=None):
    """Evaluate Multi-task Bert model

    Available eval_scheme:
        ner, cws, acc

    Keyword Arguments:
        problem {str} -- problems to evaluate (default: {'weibo_ner'})
        num_gpus {int} -- number of gpu to use (default: {1})
        model_dir {str} -- model dir (default: {''})
        eval_scheme {str} -- Evaluation scheme (default: {'ner'})
        params {Params} -- params to define model (default: {DynamicBatchSizeParams()})
        problem_type_dict {dict} -- Key: problem name, value: problem type (default: {{}})
        processing_fn_dict {dict} -- Key: problem name, value: problem data preprocessing fn (default: {{}})
    """
    params = get_params_ready(problem, num_gpus, model_dir,
                              params, problem_type_dict, processing_fn_dict, mode='predict', json_path=os.path.join(model_dir, 'params.json'))
    eval_dataset = train_eval_input_fn(params, mode=EVAL)
    one_batch_data = next(eval_dataset.as_numpy_iterator())
    mirrored_strategy = tf.distribute.MirroredStrategy()
    model = create_keras_model(
        mirrored_strategy=mirrored_strategy, params=params, mode='eval', inputs_to_build_model=one_batch_data)
    eval_dict = model.evaluate(eval_dataset, return_dict=True)
    return eval_dict


def predict_bert_multitask(
        inputs,
        problem='weibo_ner',
        model_dir='',
        params: BaseParams = None,
        problem_type_dict: Dict[str, str] = None,
        processing_fn_dict: Dict[str, Callable] = None,
        model: tf.keras.Model = None,
        return_model=False):
    """Evaluate Multi-task Bert model

    Available eval_scheme:
        ner, cws, acc

    Keyword Arguments:
        problem {str} -- problems to evaluate (default: {'weibo_ner'})
        num_gpus {int} -- number of gpu to use (default: {1})
        model_dir {str} -- model dir (default: {''})
        eval_scheme {str} -- Evaluation scheme (default: {'ner'})
        params {Params} -- params to define model (default: {DynamicBatchSizeParams()})
        problem_type_dict {dict} -- Key: problem name, value: problem type (default: {{}})
        processing_fn_dict {dict} -- Key: problem name, value: problem data preprocessing fn (default: {{}})
    """

    if params is None:
        params = DynamicBatchSizeParams()
    if not params.problem_assigned:
        if model_dir:
            base_dir, dir_name = os.path.split(model_dir)
        else:
            base_dir, dir_name = None, None
        # add new problem to params if problem_type_dict and processing_fn_dict provided
        if problem_type_dict:
            params.add_multiple_problems(
                problem_type_dict=problem_type_dict, processing_fn_dict=processing_fn_dict)
        params.from_json(os.path.join(model_dir, 'params.json'))
        params.assign_problem(problem, gpu=1,
                              base_dir=base_dir, dir_name=dir_name, predicting=True)
    else:
        print('Params problem assigned. Problem list: {0}'.format(
            params.run_problem_list))

    LOGGER.info('Checkpoint dir: %s', params.ckpt_dir)
    time.sleep(3)

    mirrored_strategy = tf.distribute.MirroredStrategy()
    if model is None:
        model = create_keras_model(
            mirrored_strategy=mirrored_strategy, params=params)
        model.load_weights(os.path.join(params.ckpt_dir, 'model'))

    pred_dataset = predict_input_fn(inputs, params)

    with mirrored_strategy.scope():
        pred = model.predict(pred_dataset)

    if return_model:
        return pred, model
    return pred


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--problem', type=str,
                        default='weibo_ner&weibo_cws', help='Problems to run')
    parser.add_argument('--schedule', type=str,
                        default='train', help='train or eval')
    parser.add_argument('--model_dir', type=str,
                        default='', help='path for saving trained models')
    parser.add_argument('--num_epochs', type=int, default=15)
    parser.add_argument('--num_gpus', type=int, default=1)

    args = parser.parse_args()

    if args.schedule == 'train':
        train_bert_multitask(
            problem=args.problem,
            model_dir=args.model_dir,
            num_gpus=args.num_gpus,
            num_epochs=args.num_epochs
        )
    else:
        eval_bert_multitask(
            problem=args.problem,
            model_dir=args.model_dir,
            num_gpus=args.num_gpus,
            eval_scheme=args.eval_scheme,
        )
