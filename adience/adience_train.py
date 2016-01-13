"""A binary to train Adience using a single GPU.

Accuracy:


Speed: With batch_size 128.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime
import os.path
import time

import tensorflow.python.platform
from tensorflow.python.platform import gfile

import numpy as np
from six.moves import xrange    # pylint: disable=redefined-builtin
import tensorflow as tf

#from tensorflow.models.image.cifar10 import cifar10
import adience

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('train_dir', '../../MLtrained',
                         """Directory where to write event logs """
                         """and checkpoint.""")
tf.app.flags.DEFINE_integer('max_steps', 100000,
                            """Number of batches to run.""")
tf.app.flags.DEFINE_boolean('log_device_placement', False,
                            """Whether to log device placement.""")


def train(train_continue):
    """Train Adience for a number of steps."""
    with tf.Graph().as_default():
        global_step = tf.Variable(0, trainable=False)

        # Get images and labels for Adience.
        images, labels = adience.distorted_inputs()
        print("distorted images")
        #print(labels)

        # Build a Graph that computes the logits predictions from the
        # inference model.
        print('call inference')
        logits = adience.inference(images)

        # Calculate loss.
        print('call loss')
        loss = adience.loss(logits, labels)

        # Build a Grahalloph that trains the model with one batch of examples and
        # updates the model parameters.
        print('train_op')
        train_op = adience.train(loss, global_step)

        # Build the summary operation based on the TF collection of Summaries.
        summary_op = tf.merge_all_summaries()

        # Build an initialization operation to run below.
        init = tf.initialize_all_variables()

        # Start running operations on the Graph.
        sess = tf.Session(config=tf.ConfigProto(
                log_device_placement=FLAGS.log_device_placement))
        sess.run(init)

        # Create a saver.
        if not train_continue:
            saver = tf.train.Saver(tf.all_variables())
            load_step = 0

        else:
            # Restore the moving average version of the learned variables for eval.
            variable_averages = tf.train.ExponentialMovingAverage(
                    adience.MOVING_AVERAGE_DECAY)
            variables_to_restore = {}
            for v in tf.all_variables():
                if v in tf.trainable_variables():
                    restore_name = variable_averages.average_name(v)
                else:
                    restore_name = v.op.name
                variables_to_restore[restore_name] = v
            saver = tf.train.Saver(variables_to_restore)

            ckpt = tf.train.get_checkpoint_state(FLAGS.train_dir)
            if ckpt and ckpt.model_checkpoint_path:
                print("Checkpoint found")
                # Restores from checkpoint
                saver.restore(sess, ckpt.model_checkpoint_path)
                # Assuming model_checkpoint_path looks something like:
                #     /my-favorite-path/cifar10_train/model.ckpt-0,
                # extract global_step from it.
                load_step = int(ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]) + 1
                print("Start from step: {}".format(load_step))

            else:
                print('No checkpoint file found')

        # Start the queue runners.
        tf.train.start_queue_runners(sess=sess)

        summary_writer = tf.train.SummaryWriter(FLAGS.train_dir, graph_def=sess.graph_def)

        for step in xrange(FLAGS.max_steps - load_step):
            # continue
            step += load_step

            start_time = time.time()
            _, loss_value = sess.run([train_op, loss])
            duration = time.time() - start_time

            assert not np.isnan(loss_value), 'Model diverged with loss = NaN'

            if step % 10 == 0:
                num_examples_per_step = FLAGS.batch_size
                examples_per_sec = num_examples_per_step / duration
                sec_per_batch = float(duration)

                format_str = ('%s: step %d, loss = %.2f (%.1f examples/sec; %.3f '
                                            'sec/batch)')
                print (format_str % (datetime.now(), step, loss_value,
                                                         examples_per_sec, sec_per_batch))

            if step % 100 == 0:
                summary_str = sess.run(summary_op)
                summary_writer.add_summary(summary_str, step)

            # Save the model checkpoint periodically.
            if step % 1000 == 0 or (step + 1) == FLAGS.max_steps:
                checkpoint_path = os.path.join(FLAGS.train_dir, 'model.ckpt')
                saver.save(sess, checkpoint_path, global_step=step)

        else:
            print("Step already over limit: {}".format(FLAGS.max_steps))


def main(argv=None):    # pylint: disable=unused-argument
    #cifar10.maybe_download_and_extract()

    # Continue training or remove current training data if existing data
    if gfile.Exists(FLAGS.train_dir):
        print("Train data found")
        train_continue = None

        while train_continue == None:
            input_continue = raw_input("Continue training? (y/n): ")
            input_continue.lower()

            if input_continue == 'y' or input_continue == 'yes':
                train_continue = True
            elif input_continue == 'n' or input_continue == 'no':
                train_continue = False
            else:
                print("Wrong input, please type y or n.")

        # Continue True
        if train_continue:
            print("Continue True\n")
            train(True)

        # Continue False
        else:
            print("Continue False, delete data\n")
            gfile.DeleteRecursively(FLAGS.train_dir)
            gfile.MakeDirs(FLAGS.train_dir)
            train(False)

    # No previous train data
    else:
        print("No trainings data found\n")
        gfile.MakeDirs(FLAGS.train_dir)
        train(False)


if __name__ == '__main__':
    tf.app.run()
