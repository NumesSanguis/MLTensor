import tensorflow.python.platform
import tensorflow as tf

from os.path import join
import csv

def read_from_txt():
    data = [[[]] for x in range(5)]
    
    for i in range(5): #i = foldnumber
        header = True
        with open("data/fold_frontal_{}_data.txt".format(i)) as tsv:
            for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
                if header == True:
                    header = False
                else:
                    data[i].append([line[0], line[1], line[2], line[4]])
        data[i].pop(0) #remove empty cell from initializing
    

    #eventual path for an image data/aligned/USERNAME/landmark_aligned_face.FACEID.IMAGENAME
    #i = fold
    #j = face
    #data[i][j][0] =USERNAME
    #data[i][j][1] =IMAGENAME
    #data[i][j][2] =FACEID
    #data[i][j][3] =GENDER (not needed in path)
    #eventual path for an image data/aligned/data[i][j][0]/landmark_aligned_face.data[i][j][2].data[i][j][1]

if __name__ == '__main__':
    read_from_txt()