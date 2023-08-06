# Copyright 2020 Tobias Höfer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
"""Implements  a morphological layer that learns the rank of a rank filter operation."""
import numpy as np
import tensorflow as tf


class Morph2D(tf.keras.layers.Layer):
    """Encapsulates both a state (weights) and a transformation from inputs to
    outputs."""
    def __init__(self, **kwargs):
        """Define state and do all input-independent initualization.

        Args:
            se (tensor): Structuring element. Defaults to np.ones((3,3)).
        """
        super(Morph2D, self).__init__(**kwargs)
        #if se is None:
        self.se = tf.ones([3, 3], dtype=tf.float32)
        #else:
        #    self.se = tf.cast(tf.convert_to_tensor(se), dtype=tf.float32)
        self.se_size = [1, self.se.shape[0], self.se.shape[1], 1]
        rank_init = tf.random_normal_initializer()
        # Define rank vector as learnable weight.
        self.rank = tf.Variable(initial_value=rank_init(
            shape=(self.se.shape[0] * self.se.shape[1], ), dtype="float32"),
                                trainable=True,
                                name="rank")

    def get_config(self):
        """Defines state to enable model_load()."""
        config = super().get_config().copy()
        config.update({
            "se": self.se,
            "se_size": self.se_size,
            "rank": self.rank
        })
        return config

    def compute_output_shape(self, input_shape):
        """This transformation preserves the input dimensions."""
        return input_shape

    def call(self, inputs):
        """Define transformation from inputs to outputs."""
        # Extract sliding patches from image.
        inputs = tf.cast(inputs, tf.float32)
        image_patches = tf.image.extract_patches(inputs,
                                                 sizes=self.se_size,
                                                 strides=[1, 1, 1, 1],
                                                 rates=[1, 1, 1, 1],
                                                 padding="SAME")
        # Reshape patches to vectors.
        shape = tf.convert_to_tensor([
            tf.shape(inputs)[0], 1,
            tf.shape(inputs)[1] * tf.shape(inputs)[2],
            self.se.shape[0] * self.se.shape[1] * 1
        ])
        image_patches = tf.reshape(image_patches, shape)

        # Reshape structuring element to vector.
        se = tf.reshape(self.se,
                        [1, 1, self.se.shape[0] * self.se.shape[1] * 1, 1])
        se = tf.transpose(se, [0, 3, 1, 2])
        se = tf.tile(se, [tf.shape(inputs)[0], 1, 1, 1])

        # Process structuring element with patches.
        mul_1 = tf.multiply(image_patches, se)

        # Non-linear sort operation of processed patches.
        sorted_list = tf.sort(mul_1, axis=-1, direction="ASCENDING")

        # Transform rank vector to probabilities.
        rank = tf.nn.softmax(self.rank)

        # Multiply one-hot rank vector with sorted list. Only element at given rank is active.
        mul_2 = tf.multiply(sorted_list, rank)

        # Compute sum over rank * SL(se * patch).
        result = tf.reduce_sum(mul_2, 3)

        # Reshape results to input dims.
        result = tf.reshape(result, tf.shape(inputs))
        return result
