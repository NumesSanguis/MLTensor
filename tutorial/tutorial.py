import tensorflow as tf
import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

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
sess = tf.Session()
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