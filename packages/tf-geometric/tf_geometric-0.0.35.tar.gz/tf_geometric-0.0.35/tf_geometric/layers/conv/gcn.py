# coding=utf-8

from tf_geometric.nn.conv.gcn import gcn, gcn_cache_normed_edge
import tensorflow as tf


class GCN(tf.keras.Model):
    """
    Graph Convolutional Layer
    """

    def build(self, input_shapes):
        x_shape = input_shapes[0]
        num_features = x_shape[-1]

        self.kernel = self.add_weight("kernel", shape=[num_features, self.units],
                                      initializer="glorot_uniform", regularizer=self.kernel_regularizer)
        if self.use_bias:
            self.bias = self.add_weight("bias", shape=[self.units],
                                        initializer="zeros", regularizer=self.bias_regularizer)

    def __init__(self, units, activation=None, use_bias=True,
                 renorm=True, improved=False,
                 kernel_regularizer=None, bias_regularizer=None, *args, **kwargs):
        """

        :param units: Positive integer, dimensionality of the output space.
        :param activation: Activation function to use.
        :param use_bias: Boolean, whether the layer uses a bias vector.
        :param renorm: Whether use renormalization trick (https://arxiv.org/pdf/1609.02907.pdf).
        :param improved: Whether use improved GCN or not.
        :param kernel_regularizer: Regularizer function applied to the `kernel` weights matrix.
        :param bias_regularizer: Regularizer function applied to the bias vector.
        """
        super().__init__(*args, **kwargs)
        self.units = units

        self.acvitation = activation
        self.use_bias = use_bias

        self.kernel = None
        self.bias = None

        self.renorm = renorm
        self.improved = improved

        self.kernel_regularizer = kernel_regularizer
        self.bias_regularizer = bias_regularizer

    def cache_normed_edge(self, graph, override=False):
        gcn_cache_normed_edge(graph, self.renorm, self.improved, override=override)

    def call(self, inputs, cache=None, training=None, mask=None):
        """

        :param inputs: List of graph info: [x, edge_index, edge_weight]
        :param cache: A dict for caching A' for GCN. Different graph should not share the same cache dict.
        :return: Updated node features (x), shape: [num_nodes, units]
        """

        if len(inputs) == 3:
            x, edge_index, edge_weight = inputs
        else:
            x, edge_index = inputs
            edge_weight = None

        return gcn(x, edge_index, edge_weight, self.kernel, self.bias,
                   activation=self.acvitation, renorm=self.renorm, improved=self.improved, cache=cache)
