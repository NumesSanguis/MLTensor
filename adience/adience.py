from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
import sys

import tensorflow.python.platform
from six.moves import xrange    # pylint: disable=redefined-builtin
import tensorflow as tf

import adience_input
from tensorflow.python.platform import gfile

FLAGS = tf.app.flags.FLAGS

# Basic model parameters.
tf.app.flags.DEFINE_integer('batch_size', 128,
                            """Number of images to process in a batch.""")
tf.app.flags.DEFINE_string('data_dir', 'data/aligned',
                           """Path to the CIFAR-10 data directory.""")