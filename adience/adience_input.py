from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow.python.platform
import tensorflow as tf


def read_adience(folder_queue):

    # from folder: data/aligned/
    test = [[[None]] for x in range(5)]
    test[0][0] = ['30601258@N03', '10424815813_e94629b1ec_o.jpg', 'm']
    test[1][0] = ['114841417@N06', '12068804204_085d553238_o.jpg', 'f']
    test[2][0] = ['64504106@N06', '11831304783_488d6c3a6d_o.jpg', 'm']
    test[3][0] = ['113445054@N07', '11763777465_11d01c34ce_o.jpg', 'm']
    test[4][0] = ['115321157@N03', '12111034286_4f5bfbacea_o.jpg', 'f']
    print(test)

    return test

if __name__ == '__main__':
    read_adience('bla')