import tensorflow as tf
import adience_input

from os.path import join

data = adience_input.read_from_txt()

input_images = tf.zeros([5])
labels = tf.zeros([5])

for i in range(5):
    in_path = join("data", "aligned", data[0][i][0], "landmark_aligned_face.{}.{}.jpg".format(data[0][i][2], data[0][i][1]))
    input_images[i] = tf.image.decode_jpeg(in_path,3)
    if data[0][i][3] == 'm':
        labels[i] = 0
    elif data[0][i][3] == 'f':
        labels[i] = 1
    else:
        labels[i] = -1

# Flattened image with undefined length (None) and 784-dimensional vector
vector_size = input_images[0].height * input_images[0].width * input_images[0].channels
x = tf.placeholder("float", [None, vector_size])
# W: weights and b: biases, initialized to 0
W = tf.Variable(tf.zeros([vector_size,3]))
b = tf.Variable(tf.zeros([3]))

# Model: multiply x by W, add b, apply tf.nn.softmax
y = tf.nn.softmax(tf.matmul(x,W) + b)

# cross-entropy placeholder
y_ = tf.placeholder("float", [None,3])

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
for i in range(5):
    batch_xs, batch_ys = data.train.next_batch(100)
    sess.run(train_step, feed_dict={x: input_images[0:3], y_: labels[0:3]})
print("Finished training")

# check predicted y is same as true y_, list with booleans
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

# convert boolean list to accuracy
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

# get accuracy on test data and print
print sess.run(accuracy, feed_dict={x: input_images[4], y_: labels[4]})