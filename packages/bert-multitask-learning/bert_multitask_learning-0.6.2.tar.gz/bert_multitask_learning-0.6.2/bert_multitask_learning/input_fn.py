

from functools import partial
from itertools import tee
from typing import List, Union, Dict

import tensorflow as tf

from .bert_preprocessing.create_bert_features import (
    create_bert_features_generator, create_multimodal_bert_features_generator)
from .params import BaseParams
from .read_write_tfrecord import read_tfrecord, write_tfrecord
from .special_tokens import PREDICT, TRAIN
from .utils import infer_shape_and_type_from_dict, load_transformer_tokenizer


def element_length_func(yield_dict: Dict[str, tf.Tensor]):
    max_length = tf.shape(yield_dict['input_ids'])[0]
    return max_length


def train_eval_input_fn(params: BaseParams, mode=TRAIN) -> tf.data.Dataset:
    '''
    This function will write and read tf record for training
    and evaluation.

    Arguments:
        params {Params} -- Params objects

    Keyword Arguments:
        mode {str} -- ModeKeys (default: {TRAIN})

    Returns:
        tf Dataset -- Tensorflow dataset
    '''
    write_tfrecord(params=params)

    dataset_dict = read_tfrecord(params=params, mode=mode)

    # make sure the order is correct
    dataset_dict_keys = list(dataset_dict.keys())
    dataset_list = [dataset_dict[key] for key in dataset_dict_keys]
    weight_list = [params.problem_sampling_weight_dict[key]
                   for key in dataset_dict_keys]

    logger = tf.get_logger()
    logger.info('sampling weights: ')
    for problem_chunk_name, weight in params.problem_sampling_weight_dict.items():
        logger.info('{0}: {1}'.format(problem_chunk_name, weight))

    dataset = tf.data.experimental.sample_from_datasets(
        datasets=dataset_list, weights=weight_list)

    if mode == TRAIN:
        dataset = dataset.shuffle(params.shuffle_buffer)

    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    if params.dynamic_padding:
        dataset = dataset.apply(
            tf.data.experimental.bucket_by_sequence_length(
                element_length_func=element_length_func,
                bucket_batch_sizes=params.bucket_batch_sizes,
                bucket_boundaries=params.bucket_boundaries
            ))
    else:
        first_example = next(dataset.as_numpy_iterator())
        output_shapes, _ = infer_shape_and_type_from_dict(first_example)

        if mode == TRAIN:
            dataset = dataset.padded_batch(params.batch_size, output_shapes)
        else:
            dataset = dataset.padded_batch(params.batch_size*2, output_shapes)

    return dataset


def predict_input_fn(input_file_or_list: Union[str, List[str]],
                     params: BaseParams,
                     mode=PREDICT,
                     labels_in_input=False) -> tf.data.Dataset:
    '''Input function that takes a file path or list of string and 
    convert it to tf.dataset

    Example:
        predict_fn = lambda: predict_input_fn('test.txt', params)
        pred = estimator.predict(predict_fn)

    Arguments:
        input_file_or_list {str or list} -- file path or list of string
        params {Params} -- Params object

    Keyword Arguments:
        mode {str} -- ModeKeys (default: {PREDICT})

    Returns:
        tf dataset -- tf dataset
    '''

    # if is string, treat it as path to file
    if isinstance(input_file_or_list, str):
        inputs = open(input_file_or_list, 'r', encoding='utf8')
    else:
        inputs = input_file_or_list

    tmp_iter, inputs = tee(inputs, 2)
    first_element = next(tmp_iter)

    if labels_in_input:
        first_element, _ = first_element

    tokenizer = load_transformer_tokenizer(
        params.transformer_tokenizer_name, params.transformer_tokenizer_loading)
    if isinstance(first_element, dict) and 'a' not in first_element:
        part_fn = partial(create_multimodal_bert_features_generator, problem='',
                          label_encoder=None,
                          params=params,
                          tokenizer=tokenizer,
                          mode=mode,
                          problem_type='cls',
                          is_seq=False)
    else:
        part_fn = partial(create_bert_features_generator, problem='',
                          label_encoder=None,
                          params=params,
                          tokenizer=tokenizer,
                          mode=mode,
                          problem_type='cls',
                          is_seq=False)
    first_dict = next(part_fn(example_list=tmp_iter))

    def gen():
        for d in part_fn(example_list=inputs):
            yield d
    output_shapes, output_type = infer_shape_and_type_from_dict(first_dict)
    dataset = tf.data.Dataset.from_generator(
        gen, output_types=output_type, output_shapes=output_shapes)

    dataset = dataset.padded_batch(
        params.batch_size,
        output_shapes
    )
    # dataset = dataset.batch(config.batch_size*2)

    return dataset


# def to_serving_input(input_file_or_list, config, mode=PREDICT, tokenizer=None):
#     '''A serving input function that takes input file path or
#     list of string and apply BERT preprocessing. This fn will
#     return a data dict instead of tf dataset. Used in serving.

#     Arguments:
#         input_file_or_list {str or list} -- file path of list of str
#         config {Params} -- Params

#     Keyword Arguments:
#         mode {str} -- ModeKeys (default: {PREDICT})
#         tokenizer {tokenizer} -- Tokenizer (default: {None})
#     '''

#     # if is string, treat it as path to file
#     if isinstance(input_file_or_list, str):
#         inputs = open(input_file_or_list, 'r', encoding='utf8').readlines()
#     else:
#         inputs = input_file_or_list

#     if tokenizer is None:
#         tokenizer = load_transformer_tokenizer(
#             config.transformer_tokenizer_name)

#     data_dict = {}
#     for doc in inputs:
#         inputs_a = cluster_alphnum(doc)
#         tokens, target = tokenize_text_with_seqs(
#             tokenizer, inputs_a, None)

#         tokens_a, tokens_b, target = truncate_seq_pair(
#             tokens, None, target, config.max_seq_len)

#         tokens, segment_ids, target = add_special_tokens_with_seqs(
#             tokens_a, tokens_b, target)

#         input_mask, tokens, segment_ids, target = create_mask_and_padding(
#             tokens, segment_ids, target, config.max_seq_len)

#         input_ids = tokenizer.convert_tokens_to_ids(tokens)
#         data_dict['input_ids'] = input_ids
#         data_dict['input_mask'] = input_mask
#         data_dict['segment_ids'] = segment_ids
#         yield data_dict


# def serving_input_fn():
#     features = {
#         'input_ids': tf.compat.v1.placeholder(tf.int32, [None, None]),
#         'input_mask': tf.compat.v1.placeholder(tf.int32, [None, None]),
#         'segment_ids': tf.compat.v1.placeholder(tf.int32, [None, None])
#     }
#     return tf.estimator.export.ServingInputReceiver(features, features)
