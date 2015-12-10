import tensorflow.python.platform
import tensorflow as tf

from os.path import join
import csv


def read_adience(folder_queue):

    # from folder: data/aligned/
    test = [[[None]] for x in range(5)]
    test[0][0] = ['30601258@N03', '10424815813_e94629b1ec_o.jpg', 'm']
    test[1][0] = ['114841417@N06', '12068804204_085d553238_o.jpg', 'f']
    test[2][0] = ['64504106@N06', '11831304783_488d6c3a6d_o.jpg', 'm']
    test[3][0] = ['113445054@N07', '11763777465_11d01c34ce_o.jpg', 'm']
    test[4][0] = ['115321157@N03', '12111034286_4f5bfbacea_o.jpg', 'f']
    #print(test)
    

    # join('data', 'aligned', test[0][0][0], test[0][0][1])
    return test


def read_from_txt():
    data = [[[]]]
    
    for i in range(5): #i = foldnumber
        print(i)
        j = 0; #j is image number in fold
        with open("data/fold_frontal_{}_data.txt".format(i)) as tsv:
            for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
                try:
                    data[i].append([line[0], line[1], line[4]])
                except:
                    data[i][j][0] = 1
                    
                j+=1
    print data[0][0]
    

if __name__ == '__main__':
    read_adience('bla')
    read_from_txt()