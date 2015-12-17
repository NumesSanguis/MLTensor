import tensorflow.python.platform
import tensorflow as tf

from os.path import join
import csv

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

        print(len(self.train_data))

        #eventual path for an image data/aligned/USERNAME/landmark_aligned_face.FACEID.IMAGENAME
        #i = fold
        #j = face
        #data[i][j][0] =USERNAME
        #data[i][j][1] =IMAGENAME
        #data[i][j][2] =FACEID
        #data[i][j][3] =GENDER (not needed in path)
        #data[i][j][4] =PATH
        #eventual path for an image data/aligned/data[i][j][0]/landmark_aligned_face.data[i][j][2].data[i][j][1]

    class AdienceRecord(object):
        pass

    def read_adience(self):
        self.filepath_queue = tf.train.string_input_producer(self.train_data)

        reader = tf.FixedLengthRecordReader(record_bytes=60)
        key, value = reader.read(self.filepath_queue)
        print(key.get_shape().as_list())
        print(value.get_shape().as_list())

        #result.label = tf.cast(train_data[i?][3]), tf.int32)
        #result = AdienceRecord()
        #result.image = 

if __name__ == '__main__':
    ad = DataInput()
    ad.read_from_txt()
    ad.read_adience()