# Moet nog aangepast worden

import tensorflow as tf
import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
sess = tf.InteractiveSession()

# Flattened image with undefined length (None) and 784-dimensional vector
x = tf.placeholder("float", [None, 784])
# W: weights and b: biases, initiliazed to 0
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))

# Model: multiply x by W, add b, apply tf.nn.softmax
y = tf.nn.softmax(tf.matmul(x,W) + b)

# cross-entropy placeholder
y_ = tf.placeholder("float", [None,10])

# cross-entropy implemented
cross_entropy = -tf.reduce_sum(y_*tf.log(y))

# optimization algorithm to modify the variables and reduce the cost
# minimize cross_entropy using gradient descent algorithm with learning rate 0.01
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

# init variables created
init = tf.initialize_all_variables()

# launch model in a Session
#sess = tf.Session()
sess.run(init)

# Train
print("Start training")
for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
print("Finished training")

# check predicted y is same as true y_, list with booleans
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

# convert boolean list to accuracy
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

# get accuracy on test data and print
print sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels})


#   Expert tutorial
print("\nExpert part\n")
# Weight Initialization
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

# Convolution and Pooling
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

# First Convolutional Layer
W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])

x_image = tf.reshape(x, [-1,28,28,1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

# Second Convolutional Layer
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

# Densely Connected Layer
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# Dropout (reduce overfitting)
keep_prob = tf.placeholder("float")
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# Readout Layer
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)


#   Train and Evaluate the Model
# steepest gradient descent optimizer --> ADAM optimizer
cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
sess.run(tf.initialize_all_variables())
for i in range(3000):
    batch = mnist.train.next_batch(50)
    if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
        print("step %d, training accuracy %g"%(i, train_accuracy))
    train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

print("test accuracy %g"%accuracy.eval(feed_dict={
    x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))

for i in range(4):
    batch = mnist.test.next_batch(50)
    test_accuracy = accuracy.eval(feed_dict={x:batch[0], y_: batch[1], keep_prob: 1.0})
    print("step %d, test accuracy %g"%(i, test_accuracy))
    








