# Author: Ankush Gupta
# Date: 2015

"""
Visualize the generated localization synthetic
data stored in h5 data-bases
"""
from __future__ import division
import os
import os.path as osp
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt 
import h5py 
from common import *



def viz_textbb(k,text_im, charBB_list, wordBB, alpha=1.0):
    """
    text_im : image containing text
    charBB_list : list of 2x4xn_i bounding-box matrices
    wordBB : 2x4xm matrix of word coordinates
    """


    plt.close(1)
    plt.figure(1)
    plt.imshow(text_im)
    plt.axis('off')
    plt.hold(True)
    # H,W = text_im.shape[:2]

    # # plot the character-BB:
    # for i in xrange(len(charBB_list)):
    #     bbs = charBB_list[i]
    #     ni = bbs.shape[-1]
    #     for j in xrange(ni):
    #         bb = bbs[:,:,j]
    #         bb = np.c_[bb,bb[:,0]]
    #         plt.plot(bb[0,:], bb[1,:], 'r', alpha=alpha/2)


    # plot the word-BB:
    for i in xrange(wordBB.shape[-1]):
        bb = wordBB[:,:,i]
        bb = np.c_[bb,bb[:,0]]
        plt.plot(bb[0,:], bb[1,:], 'b', alpha=alpha)
        # print bb
        # # visualize the indiv vertices:
        # vcol = ['r','g','b','k']  # upper left, upper right, bottom left, bottom right
        # for j in xrange(4):
        #     plt.scatter(bb[0,j],bb[1,j],color=vcol[j])


    # plt.gca().set_xlim([0,W-1])
    # plt.gca().set_ylim([H-1,0])
    # plt.show(block=False)

    plt.gca().xaxis.set_major_locator(plt.NullLocator()) 
    plt.gca().yaxis.set_major_locator(plt.NullLocator()) 
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0) 
    plt.margins(0,0)
    plt.tight_layout(pad=0)
    plt.savefig('./results/visualization/'+k.strip('_0'),bbox_inches='tight',pad_inches=0.0, dpi=300)

def main(db_fname):
    db = h5py.File(db_fname, 'r')
    dsets = sorted(db['data'].keys())
    print "total number of images : ", colorize(Color.RED, len(dsets), highlight=True)
    for i, k in enumerate(dsets):
        rgb = db['data'][k][...]
        charBB = db['data'][k].attrs['charBB']
        wordBB = db['data'][k].attrs['wordBB']
        txt = db['data'][k].attrs['txt']
        color=db['data'][k].attrs['text_color']
        font=db['data'][k].attrs['font']

        viz_textbb(k, rgb, [charBB], wordBB)
        print "image name        : ", colorize(Color.RED, k, bold=True)
        print "  ** no. of chars : ", colorize(Color.YELLOW, charBB.shape[-1])
        print "  ** no. of words : ", colorize(Color.YELLOW, wordBB.shape[-1])
        print "  ** text         : ", colorize(Color.GREEN, txt)
        print "  ** text_color   : ", colorize(Color.GREEN, color)
        print "  ** font         : ", colorize(Color.GREEN, font)

        # print wordBB

        # if 'q' in raw_input("next? ('q' to exit) : "):
        #     break

        # if i % 5 == 0:
        #     break

    db.close()

if __name__=='__main__':
    main('results/SynthText.h5')

