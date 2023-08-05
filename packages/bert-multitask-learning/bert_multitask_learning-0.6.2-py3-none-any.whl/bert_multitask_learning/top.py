import logging
from functools import partial
from typing import Dict, Tuple, Union

import tensorflow as tf
import tensorflow_addons as tfa
import transformers
from transformers.modeling_tf_utils import TFSharedEmbeddings
from tensorflow_addons.layers.crf import CRF
from tensorflow_addons.text.crf import crf_log_likelihood


from bert_multitask_learning.params import BaseParams

from .top_utils import gather_indexes


@tf.function
def empty_tensor_handling_loss(labels, logits, loss_fn):
    if tf.equal(tf.size(labels), 0):
        return 0.0
    if tf.equal(tf.size(tf.shape(labels)), 0):
        return 0.0
    if tf.equal(tf.shape(labels)[0], 0):
        return 0.0
    else:
        return tf.reduce_mean(loss_fn(
            labels, logits, from_logits=True))


@tf.function
def nan_loss_handling(loss):
    if tf.math.is_nan(loss):
        return 0.0
    else:
        return loss


@tf.function
def create_dummy_if_empty(inp_tensor: tf.Tensor) -> tf.Tensor:
    shape_tensor = tf.shape(inp_tensor)
    if tf.equal(shape_tensor[0], 0):
        data_type = inp_tensor.dtype
        dummy_shape_first_dim = tf.convert_to_tensor([1], dtype=tf.int32)
        dummy_shape = tf.concat(
            [dummy_shape_first_dim, shape_tensor[1:]], axis=0)
        dummy_tensor = tf.zeros(dummy_shape, dtype=data_type)
        return dummy_tensor
    else:
        return inp_tensor


class BaseTop(tf.keras.Model):
    def __init__(self, params: BaseParams, problem_name: str) -> None:
        super(BaseTop, self).__init__(name=problem_name)
        self.params = params
        self.problem_name = problem_name

    def call(self, inputs: Tuple[Dict], mode: str):
        raise NotImplementedError


class SequenceLabel(tf.keras.Model):
    def __init__(self, params: BaseParams, problem_name: str):
        super(SequenceLabel, self).__init__(name=problem_name)
        self.params = params
        self.problem_name = problem_name
        num_classes = self.params.num_classes[self.problem_name]
        self.dense = tf.keras.layers.Dense(num_classes, activation=None)

        self.dropout = tf.keras.layers.Dropout(1-params.dropout_keep_prob)

        if self.params.crf:
            self.crf = CRF(num_classes)
            self.metric_fn = tf.keras.metrics.Accuracy(
                name='{}_acc'.format(self.problem_name)
            )
        else:
            self.metric_fn = tf.keras.metrics.SparseCategoricalAccuracy(
                name='{}_acc'.format(self.problem_name))

    def return_crf_result(self, labels: tf.Tensor, logits: tf.Tensor, mode: str, input_mask: tf.Tensor):
        input_mask.set_shape([None, None])
        logits = create_dummy_if_empty(logits)
        input_mask = create_dummy_if_empty(input_mask)
        viterbi_decoded, potentials, sequence_length, chain_kernel = self.crf(
            logits, input_mask)
        if mode != tf.estimator.ModeKeys.PREDICT:
            loss = -crf_log_likelihood(potentials,
                                       labels, sequence_length, chain_kernel)[0]
            loss = tf.reduce_mean(loss)
            loss = nan_loss_handling(loss)
            self.add_loss(loss)
            acc = self.metric_fn(
                labels, viterbi_decoded, sample_weight=input_mask)
            self.add_metric(acc)

        # make the crf prediction has the same shape as non-crf prediction
        return tf.one_hot(viterbi_decoded, name='%s_predict' % self.problem_name, depth=self.params.num_classes[self.problem_name])

    def call(self, inputs, mode):
        training = (mode == tf.estimator.ModeKeys.TRAIN)
        feature, hidden_feature = inputs
        hidden_feature = hidden_feature['seq']
        if mode != tf.estimator.ModeKeys.PREDICT:
            labels = feature['{}_label_ids'.format(self.problem_name)]
            # sometimes the length of labels dose not equal to length of inputs
            # that's caused by tf.data.experimental.bucket_by_sequence_length in multi problem scenario
            pad_len = tf.shape(input=hidden_feature)[
                1] - tf.shape(input=labels)[1]

            # top, bottom, left, right
            pad_tensor = [[0, 0], [0, pad_len]]
            labels = tf.pad(tensor=labels, paddings=pad_tensor)

        else:
            labels = None
        hidden_feature = self.dropout(hidden_feature, training)

        if self.params.crf:
            return self.return_crf_result(labels, hidden_feature, mode, feature['model_input_mask'])

        logits = self.dense(hidden_feature)

        if mode != tf.estimator.ModeKeys.PREDICT:
            loss = empty_tensor_handling_loss(
                labels, logits,
                tf.keras.losses.sparse_categorical_crossentropy)
            self.add_loss(loss)
            acc = self.metric_fn(
                labels, logits, sample_weight=feature['model_input_mask'])
            self.add_metric(acc)
        return tf.nn.softmax(
            logits, name='%s_predict' % self.problem_name)


class Classification(tf.keras.layers.Layer):
    def __init__(self, params: BaseParams, problem_name: str) -> None:
        super(Classification, self).__init__(name=problem_name)
        self.params = params
        self.problem_name = problem_name
        num_classes = self.params.num_classes[self.problem_name]
        self.dense = tf.keras.layers.Dense(num_classes, activation=None)
        self.metric_fn = tf.keras.metrics.SparseCategoricalAccuracy(
            name='{}_acc'.format(self.problem_name))

        self.dropout = tf.keras.layers.Dropout(1-params.dropout_keep_prob)

    def call(self, inputs, mode):
        training = (mode == tf.estimator.ModeKeys.TRAIN)
        feature, hidden_feature = inputs
        hidden_feature = hidden_feature['pooled']
        if mode != tf.estimator.ModeKeys.PREDICT:
            labels = feature['{}_label_ids'.format(self.problem_name)]
        else:
            labels = None
        hidden_feature = self.dropout(hidden_feature, training)
        logits = self.dense(hidden_feature)

        if mode != tf.estimator.ModeKeys.PREDICT:
            labels = tf.squeeze(labels)
            # convert labels to one-hot to use label_smoothing
            one_hot_labels = tf.one_hot(
                labels, depth=self.params.num_classes[self.problem_name])
            loss_fn = partial(tf.keras.losses.categorical_crossentropy,
                              from_logits=True, label_smoothing=self.params.label_smoothing)

            loss = empty_tensor_handling_loss(
                one_hot_labels, logits,
                loss_fn)
            loss = nan_loss_handling(loss)
            self.add_loss(loss)
            acc = self.metric_fn(labels, logits)
            self.add_metric(acc)
        return tf.nn.softmax(
            logits, name='%s_predict' % self.problem_name)


class PreTrain(tf.keras.Model):
    def __init__(self, params: BaseParams, problem_name: str, input_embeddings: tf.Tensor):
        super(PreTrain, self).__init__(name=problem_name)
        self.params = params
        self.nsp = transformers.modeling_tf_bert.TFBertNSPHead(
            self.params.bert_config)

        # TODO: add mlm back to pretrain
        self.mlm = transformers.modeling_tf_bert.TFBertMLMHead(
            self.params.bert_config, input_embeddings=input_embeddings)

    def call(self,
             inputs: Tuple[Dict[str, Dict[str, tf.Tensor]], Dict[str, Dict[str, tf.Tensor]]],
             mode: str) -> Tuple[tf.Tensor, tf.Tensor]:
        features, hidden_features = inputs

        # compute logits
        nsp_logits = self.nsp(hidden_features['pooled'])

        # masking is done inside the model
        seq_hidden_feature = hidden_features['seq']
        positions = features['masked_lm_positions']

        # gather_indexes will flatten the seq hidden_states, we need to reshape
        # back to 3d tensor
        input_tensor = gather_indexes(seq_hidden_feature, positions)
        shape_tensor = tf.shape(positions)
        shape_list = tf.concat([shape_tensor, [-1]], axis=0)
        input_tensor = tf.reshape(input_tensor, shape=shape_list)
        # set_shape to determin rank
        input_tensor.set_shape(
            [None, None, seq_hidden_feature.shape.as_list()[-1]])
        mlm_logits = self.mlm(input_tensor)

        if mode != tf.estimator.ModeKeys.PREDICT:
            nsp_labels = tf.squeeze(
                features['next_sentence_label_ids'])
            mlm_labels = features['masked_lm_ids']
            mlm_labels.set_shape([None, None])
            # compute loss
            nsp_loss = empty_tensor_handling_loss(
                nsp_labels, nsp_logits,
                tf.keras.losses.sparse_categorical_crossentropy)
            mlm_loss_layer = transformers.modeling_tf_utils.TFMaskedLanguageModelingLoss()
            # mlm_loss = tf.reduce_mean(
            #     mlm_loss_layer.compute_loss(mlm_labels, mlm_logits))

            # add a useless from_logits argument to match the function signature of keras losses.
            def loss_fn_wrapper(labels, logits, from_logits=True):
                return mlm_loss_layer.compute_loss(labels, logits)
            mlm_loss = empty_tensor_handling_loss(
                mlm_labels,
                mlm_logits,
                loss_fn_wrapper
            )
            loss = nsp_loss + mlm_loss
            self.add_loss(loss)

        return (tf.sigmoid(nsp_logits), tf.nn.softmax(mlm_logits))


class Seq2Seq(tf.keras.Model):
    def __init__(self, params: BaseParams, problem_name: str, input_embeddings: tf.keras.layers.Layer):
        super(Seq2Seq, self).__init__(name=problem_name)
        # self.params = params
        # self.problem_name = problem_name
        # # if self.params.init_weight_from_huggingface:
        # #     self.decoder = load_transformer_model(
        # #         self.params.transformer_decoder_model_name,
        # #         self.params.transformer_decoder_model_loading)
        # # else:
        # #     self.decoder = load_transformer_model(
        # #         self.params.bert_decoder_config, self.params.transformer_decoder_model_loading)

        # # TODO: better implementation
        # logging.warning(
        #     'Seq2Seq model is not well supported yet. Bugs are expected.')
        # config = self.params.bert_decoder_config
        # # some hacky approach to share embeddings from encoder to decoder
        # word_embedding_weight = input_embeddings.word_embeddings
        # self.vocab_size = word_embedding_weight.shape[0]
        # self.share_embedding_layer = TFSharedEmbeddings(
        #     vocab_size=word_embedding_weight.shape[0], hidden_size=word_embedding_weight.shape[1])
        # self.share_embedding_layer.build([1])
        # self.share_embedding_layer.weight = word_embedding_weight
        # # self.decoder = TFBartDecoder(
        # #     config=config, embed_tokens=self.share_embedding_layer)
        # self.decoder = TFBartDecoderForConditionalGeneration(
        #     config=config, embedding_layer=self.share_embedding_layer)
        # self.decoder.set_bos_id(self.params.bos_id)
        # self.decoder.set_eos_id(self.params.eos_id)

        # self.metric_fn = tf.keras.metrics.SparseCategoricalAccuracy(
        #     name='{}_acc'.format(self.problem_name))
        raise NotImplementedError

    def _seq2seq_label_shift_right(self, labels: tf.Tensor, eos_id: int) -> tf.Tensor:
        batch_eos_ids = tf.fill([tf.shape(labels)[0], 1], eos_id)
        batch_eos_ids = tf.cast(batch_eos_ids, dtype=tf.int64)
        decoder_lable = labels[:, 1:]
        decoder_lable = tf.concat([decoder_lable, batch_eos_ids], axis=1)
        return decoder_lable

    def call(self,
             inputs: Tuple[Dict[str, Dict[str, tf.Tensor]], Dict[str, Dict[str, tf.Tensor]]],
             mode: str):
        features, hidden_features = inputs
        encoder_mask = features['model_input_mask']

        if mode == tf.estimator.ModeKeys.PREDICT:
            input_ids = None
            decoder_padding_mask = None
        else:
            input_ids = features['%s_label_ids' % self.problem_name]
            decoder_padding_mask = features['{}_mask'.format(
                self.problem_name)]

        if mode == tf.estimator.ModeKeys.PREDICT:
            return self.decoder.generate(eos_token_id=self.params.eos_id, encoder_hidden_states=hidden_features['seq'])
        else:
            decoder_output = self.decoder(input_ids=input_ids,
                                          encoder_hidden_states=hidden_features['seq'],
                                          encoder_padding_mask=encoder_mask,
                                          decoder_padding_mask=decoder_padding_mask,
                                          decode_max_length=self.params.decode_max_seq_len,
                                          mode=mode)
            loss = decoder_output.loss
            logits = decoder_output.logits
            self.add_loss(loss)
            decoder_label = self._seq2seq_label_shift_right(
                features['%s_label_ids' % self.problem_name], eos_id=self.params.eos_id)
            acc = self.metric_fn(decoder_label, logits)
            self.add_metric(acc)
            return logits


class MultiLabelClassification(tf.keras.Model):
    def __init__(self, params: BaseParams, problem_name: str) -> None:
        super(MultiLabelClassification, self).__init__(name=problem_name)
        self.params = params
        self.problem_name = problem_name
        self.dense = tf.keras.layers.Dense(
            self.params.num_classes[problem_name])
        self.dropout = tf.keras.layers.Dropout(
            1-self.params.dropout_keep_prob
        )
        self.metric_fn = tfa.metrics.F1Score(
            num_classes=self.params.num_classes[problem_name],
            threshold=self.params.multi_cls_threshold,
            average='macro',
            name='{}_f1'.format(problem_name))

    def call(self, inputs, mode):
        training = (mode == tf.estimator.ModeKeys.TRAIN)
        feature, hidden_feature = inputs
        hidden_feature = hidden_feature['pooled']
        if mode != tf.estimator.ModeKeys.PREDICT:
            labels = feature['{}_label_ids'.format(self.problem_name)]
        else:
            labels = None
        hidden_feature = self.dropout(hidden_feature, training)
        logits = self.dense(hidden_feature)

        if mode != tf.estimator.ModeKeys.PREDICT:
            labels = tf.squeeze(labels)
            labels = tf.cast(labels, tf.float32)
            # use weighted loss
            label_weights = self.params.multi_cls_positive_weight

            def _loss_fn_wrapper(x, y, from_logits=True):
                return tf.nn.weighted_cross_entropy_with_logits(x, y, pos_weight=label_weights, name='{}_loss'.format(self.problem_name))
            loss = empty_tensor_handling_loss(
                labels, logits, _loss_fn_wrapper)
            loss = nan_loss_handling(loss)
            self.add_loss(loss)
            labels = create_dummy_if_empty(labels)
            logits = create_dummy_if_empty(logits)
            f1 = self.metric_fn(labels, logits)
            self.add_metric(f1)

        return tf.nn.sigmoid(
            logits, name='%s_predict' % self.problem_name)


class MaskLM(tf.keras.Model):
    """Multimodal MLM top layer.
    """

    def __init__(self, params: BaseParams, problem_name: str, input_embeddings: tf.keras.layers.Layer) -> None:
        super(MaskLM, self).__init__(name=problem_name)
        self.params = params
        self.problem_name = problem_name

        word_embedding_weight = input_embeddings.word_embeddings
        self.vocab_size = word_embedding_weight.shape[0]
        self.share_embedding_layer = TFSharedEmbeddings(
            vocab_size=word_embedding_weight.shape[0], hidden_size=word_embedding_weight.shape[1])
        self.share_embedding_layer.build([1])
        self.share_embedding_layer.weight = word_embedding_weight

    def call(self, inputs, mode):
        features, hidden_features = inputs

        # masking is done inside the model
        seq_hidden_feature = hidden_features['seq']
        positions = features['masked_lm_positions']

        # gather_indexes will flatten the seq hidden_states, we need to reshape
        # back to 3d tensor
        input_tensor = gather_indexes(seq_hidden_feature, positions)
        shape_tensor = tf.shape(positions)
        shape_list = tf.concat([shape_tensor, [-1]], axis=0)
        input_tensor = tf.reshape(input_tensor, shape=shape_list)
        # set_shape to determin rank
        input_tensor.set_shape(
            [None, None, seq_hidden_feature.shape.as_list()[-1]])
        mlm_logits = self.share_embedding_layer(input_tensor, mode='linear')
        if mode != tf.estimator.ModeKeys.PREDICT:
            mlm_labels = features['masked_lm_ids']
            mlm_labels.set_shape([None, None])
            # compute loss
            mlm_loss = empty_tensor_handling_loss(
                mlm_labels,
                mlm_logits,
                tf.keras.losses.sparse_categorical_crossentropy
            )
            loss = nan_loss_handling(mlm_loss)
            self.add_loss(loss)

        return tf.nn.softmax(mlm_logits)
