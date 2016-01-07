import tensorflow.python.platform
import tensorflow as tf
from PIL import Image
import numpy as np
from os.path import join
import csv
from scipy import misc

KNOWN_HEIGHT = 812
KNOWN_WIDTH = 812

class DataInput():
    def __init__(self):
        pass

    def read_from_txt(self):
        #self.data = [[[]] for x in range(5)]
        img_path = [[] for x in range(5)]
        img_label = [[] for x in range(5)]
        
        for i in range(5): #i = foldnumber
            header = True
            with open("data/fold_frontal_{}_data.txt".format(i)) as tsv:
                for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
                    if header == True:
                        header = False
                    else:
                        img_path[i].append(join('data','aligned',line[0],'landmark_aligned_face.{}.{}.jpg'.format(line[2],line[1])))
                        img_label[i].append(line[4])
                        #self.data[i].append([line[0], line[1], line[2], line[4], join('data','aligned',line[0],'landmark_aligned_face.{}.{}.jpg'.format(line[2],line[1])) ])
            img_path[i].pop(0)
            img_label[i].pop(0)
            #self.data[i].pop(0) #remove empty cell from initializing
        #self.train_data = self.data[0] + self.data[1] + self.data[2] + self.data[3]
        self.train_data = img_path[0] + img_path[1] + img_path[2] + img_path[3]
        self.train_label = img_label[0] + img_label[1] + img_label[2] + img_label[3]

        print("len train data: {}".format(len(self.train_data)))

        #eventual path for an image data/aligned/USERNAME/landmark_aligned_face.FACEID.IMAGENAME
        #i = fold
        #j = face
        #data[i][j][0] =USERNAME
        #data[i][j][1] =IMAGENAME
        #data[i][j][2] =FACEID
        #data[i][j][3] =GENDER (not needed in path)
        #data[i][j][4] =PATH
        #eventual path for an image data/aligned/data[i][j][0]/landmark_aligned_face.data[i][j][2].data[i][j][1]



    def read_adience(self):

        class AdienceRecord(object):
            pass
        result = AdienceRecord()

        # img = misc.imread('./test.jpg')
        # print img.shape    # (32, 32, 3)
        #
        # img_tf = tf.Variable(img)
        # print(img_tf)
        # print img_tf.get_shape().as_list()  # [32, 32, 3]

        string = ['mtest.jpg', 'ftest2.jpg']  # , 'test2.jpg' '/home/marcel/work1.jpg'
        labels = ['m', 'f']
        filepath_queue = tf.train.string_input_producer(string)

        self.reader = tf.WholeFileReader()
        result.key, value = self.reader.read(filepath_queue)
        print("going to slice")
        result.label = tf.slice(value, 0, 1)
        imgpath = 'bla'  # value[1:]


        print("label: {}".format(result.label))
        print("imgpath: {}".format(imgpath))
        print("key: {}".format(result.key))

        # img = misc.imread(value)
        # print img.shape    # (32, 32, 3)
        # img_tf = tf.Variable(img)


        my_img = tf.image.decode_jpeg(imgpath, channels=3)
        my_img.set_shape([KNOWN_HEIGHT, KNOWN_WIDTH, 3])
        print(my_img)

        result.image = my_img

        return(result)

        # sess = tf.Session()
        # plaatje = Image.open(sess.run(value))
        # plaatje.show()

        # sess = tf.Session()
        # c = tf.constant(5.0)
        # print(sess.run(c))
        #print(sess.run(value))

        # init = tf.initialize_all_variables()
        # with tf.Session() as sess:
        #     sess.run(init)
        #     v = sess.run(value)
        #     print(v)


        # my_img_enc = tf.image.encode_jpeg(my_img)
        # print(my_img_enc)
        #my_img_enc.show()


        # init_op = tf.initialize_all_variables()
        # with tf.Session() as sess:
        #     sess.run(init_op)
        #
        #     # Start populating the filename queue.
        #
        #     coord = tf.train.Coordinator()
        #     threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        #
        #     try:
        #         # while not coord.should_stop():
        #         image = my_img.eval()
        #         print(image.shape)
        #             #Image.show(Image.fromarray(np.asarray(image)))
        #
        #     except(tf.errors.OutOfRangeError):
        #         print('Done training -- epoch limit reached')
        #
        #     finally:
        #         # When done, ask the threads to stop.
        #         coord.request_stop()
        #
        #     # for i in range(1): #length of your filename list
        #     #   image = my_img.eval() #here is your image Tensor :)
        #     #
        #     # print(image.shape)
        #     #Image.show(Image.fromarray(np.asarray(image)))
        #
        #     # Wait for threads to finish.
        #     coord.join(threads)
        #     sess.close()

            # coord.request_stop()
            # coord.join(threads)


        #
        # #float_img = tf.cast(img, tf.float32)
        # # tf.image_summary('img', float_img)
        # #
        # # sess = tf.Session()
        # # summary_op = tf.merge
        #
        #print(key)
        # print(value)
        # print(my_img.get_shape().as_list())

        # init = tf.initialize_all_variables()
        # sess = tf.Session()
        # sess.run(init)
        # im = sess.run(img_tf)
        #
        # import matplotlib.pyplot as plt
        # fig = plt.figure()
        # fig.add_subplot(1,2,1)
        # plt.imshow(im)
        # fig.add_subplot(1,2,2)
        # plt.imshow(img)
        # plt.show()




if __name__ == '__main__':
    ad = DataInput()
    ad.read_from_txt()
    ad.read_adience()