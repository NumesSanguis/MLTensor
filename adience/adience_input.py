import tensorflow.python.platform
import tensorflow as tf
from PIL import Image
import numpy as np
from os.path import join
import csv
import sys

KNOWN_HEIGHT = 64
KNOWN_WIDTH = 64

class DataInput():
    def __init__(self):
        pass

    def read_from_txt(self):
        #self.data = [[[]] for x in range(5)]
        img_path = [[] for x in range(5)]
        img_label = [[] for x in range(5)]
        img_string_que = [[] for x in range(5)]
        
        for i in range(5): #i = foldnumber
            header = True
            with open("data/fold_frontal_{}_data.txt".format(i)) as tsv:
                for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
                    if header == True:
                        header = False
                    else:
                        if line[4] and line[4] != 'u': #needed to remove images without label
                            if line[4] == 'm': # 0 men
                                img_string_que[i].append(join('data','aligned',line[0],'landmark_aligned_face.{}.{},{}'.format(line[2],line[1],0)))
                                img_label[i].append(0)
                            elif line[4] == 'f':  # 1 women
                                img_string_que[i].append(join('data','aligned',line[0],'landmark_aligned_face.{}.{},{}'.format(line[2],line[1],1)))
                                img_label[i].append(1)
                            else:
                                print("abort")
                                print(line[4])
                                sys.exit()

                            img_path[i].append(join('data','aligned',line[0],'landmark_aligned_face.{}.{}'.format(line[2],line[1])))
                        #self.data[i].append([line[0], line[1], line[2], line[4], join('data','aligned',line[0],'landmark_aligned_face.{}.{}.jpg'.format(line[2],line[1])) ])
            img_path[i].pop(0)
            img_label[i].pop(0)
            img_string_que[i].pop(0)
            #self.data[i].pop(0) #remove empty cell from initializing
        #self.train_data = self.data[0] + self.data[1] + self.data[2] + self.data[3]
        self.train_data = img_path[0] + img_path[1] + img_path[2] + img_path[3]
        self.train_label = img_label[0] + img_label[1] + img_label[2] + img_label[3]
        self.train_string_que = img_string_que[0] + img_string_que[1] + img_string_que[2] + img_string_que[3]

        # Test data
        self.eval_data = img_path[4]
        self.eval_label = img_label[4]
        self.eval_string_que = img_string_que[4]


        # Smaller train queue

        #self.train_string_que = self.train_string_que[:10]

        print("len train data: {}".format(len(self.train_data)))
        print("len file que data: {}".format(len(self.train_string_que)))
        print(self.train_string_que[-1])
        print(self.train_data[-1])
        print(self.train_label[-1])
        print('done reading data from txt files')

        #eventual path for an image data/aligned/USERNAME/landmark_aligned_face.FACEID.IMAGENAME
        #i = fold
        #j = face
        #data[i][j][0] =USERNAME
        #data[i][j][1] =IMAGENAME
        #data[i][j][2] =FACEID
        #data[i][j][3] =GENDER (not needed in path)
        #data[i][j][4] =PATH
        #eventual path for an image data/aligned/data[i][j][0]/landmark_aligned_face.data[i][j][2].data[i][j][1]


    def read_my_file_format(self, filename_and_label_tensor):
        """Consumes a single filename and label as a ' '-delimited string.

        Args:
          filename_and_label_tensor: A scalar string tensor.

        Returns:
          Two tensors: the decoded image, and the string label.
        """
        filename, label = tf.decode_csv(filename_and_label_tensor, [[""], []], ",")
        # cast label to int32
        label = tf.cast(label, tf.int32)
        #print(label)

        file_contents = tf.read_file(filename)
        image = tf.image.decode_jpeg(file_contents)
        image.set_shape([KNOWN_HEIGHT, KNOWN_WIDTH, 3])

        return image, label


    def read_adience(self):

        class AdienceRecord(object):
            pass
        result = AdienceRecord()

        print(self.train_string_que[0])
        print(self.train_string_que[-1])
        #print(string)

        print('start reading adience')
        #string = ['test.jpg,m', 'test2.jpg,f']  # , 'test2.jpg' '/home/marcel/work1.jpg'

        filepath_queue = tf.train.string_input_producer(self.train_string_que)
        result.dec_image, result.label = self.read_my_file_format(filepath_queue.dequeue())

        print(result.dec_image)
        print(result.label)

        # # Test show image
        # images = []
        # with tf.Session() as sess:
        #
        #     #print(result.label.eval())
        #
        #     print('Populating filequeue')
        #     # Start populating the filename queue.
        #
        #     coord = tf.train.Coordinator()
        #     threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        #
        #     print('done populating filequeue')
        #     if len(string) > 0:
        #       for i in range(len(string)):
        #         plaatje = result.dec_image.eval()
        #         images.append(plaatje)
        #
        #     Image._showxv(Image.fromarray(np.asarray(plaatje)))
        #
        #     coord.request_stop()
        #     coord.join(threads)
        #     print("tf.session success")

        return(result)


    def read_adience_eval(self):
        print("Adience eval input")

        class AdienceRecord(object):
            pass
        result = AdienceRecord()

        print('start reading adience')
        filepath_queue = tf.train.string_input_producer(self.eval_string_que)

        result.dec_image, result.label = self.read_my_file_format(filepath_queue.dequeue())

        print(result.dec_image)
        print(result.label)
        print("Adience eval input done")

        return(result)


if __name__ == '__main__':
    ad = DataInput()
    ad.read_from_txt()
    ad.read_adience()