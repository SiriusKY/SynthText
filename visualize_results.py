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
import math
import json



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
        print ('bb:',bb)
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


# def get_words(txt):
#     words=[]
#     for t in range(len(txt)):
#         t.replace('\n',' ')
#         ws=t.split(' ')
#         for w in ws:
#             words.append(w)
#     return words


def savejson_textbb(txt, wordBB, global_bbox_id, color, font, area, image_id):
    local_bbox_id=0
    annDicts=[]
    for i, t in enumerate(txt):
        t=t.replace('\n',' ')
        ws=t.split(' ')
        for w in ws:
            if w == '  ' or w == ' ' or w == '':
                i-=1
                continue
            print('-------------------------- bbox detail -----------------------------')
            print "  *** global_bbox_id     : ", colorize(Color.YELLOW, global_bbox_id)
            print "  *** local_bbox_id     : ", colorize(Color.YELLOW, local_bbox_id)
            local_bbox_id+=1
            global_bbox_id+=1
            print "  *** text     : ", colorize(Color.YELLOW, w)

            bb = wordBB[:,:,local_bbox_id-1]
            bb = np.c_[bb,bb[:,0]]
            bbox=[]
            bbox.append(round(bb[0,0],1))
            bbox.append(round(bb[1,0],1))
            theta=math.atan((bb[1,0]-bb[1,1])/(bb[0,1]-bb[0,0]))
            bbox_width=(bb[0,1]-bb[0,0])/math.cos(theta)
            bbox_height=(bb[1,2]-bb[1,1])/math.cos(theta)
            bbox.append(round(bbox_width,1))
            bbox.append(round(bbox_height,1))
            bbox.append(round(theta,3))
            print "  *** bbox     : ", colorize(Color.YELLOW, bbox)
            segmentation=[[round(bb[0,0],1),round(bb[1,0],1), round(bb[0,1],1),round(bb[1,1],1), \
                            round(bb[0,2],1), round(bb[1,2],1),round(bb[0,3],1),round(bb[1,3],1)]]
            print "  *** seg      : ", colorize(Color.YELLOW, segmentation)
            print "  *** color     : ", colorize(Color.YELLOW, color[i])
            if font[i][0]==1:
                print "  *** font     : ", colorize(Color.YELLOW, 'is_italic')
            else:
                print "  *** font     : ", colorize(Color.YELLOW, 'not_italic')
            if font[i][1]==1:
                print "  *** font     : ", colorize(Color.YELLOW, 'is_bold')
            else:
                print "  *** font     : ", colorize(Color.YELLOW, 'not_bold')
            if font[i][2]==1:
                print "  *** font     : ", colorize(Color.YELLOW, 'serif')
            else:
                print "  *** font     : ", colorize(Color.YELLOW, 'sans_serif')
            
            tmpAnnDict={}
            tmpAnnDict['segmentation']=segmentation
            tmpAnnDict['category_id']=1
            tmpAnnDict['area']=area
            tmpAnnDict['iscrowd']=0
            tmpAnnDict['image_id']=image_id+1
            tmpAnnDict['id']=global_bbox_id
            tmpAnnDict['bbox']=bbox
            tmpAnnDict['content']=w
            tmpAnnDict['color']=color[i].tolist()
            tmpAnnDict['is_italic']=font[i][0]
            tmpAnnDict['is_bold']=font[i][1]
            tmpAnnDict['font']=font[i][2]
            annDicts.append(tmpAnnDict)
            print('-------------------------end of bbox detail -------------------------')
    return annDicts, global_bbox_id


def main(db_fname):
    db = h5py.File(db_fname, 'r')
    dsets = sorted(db['data'].keys())
    print "total number of images : ", colorize(Color.RED, len(dsets), highlight=True)

    
    global_bbox_id=0

    imDicts = []
    annDicts = []
    cateDicts = []

    for image_id, k in enumerate(dsets):
        rgb = db['data'][k][...]
        charBB = db['data'][k].attrs['charBB']
        wordBB = db['data'][k].attrs['wordBB']
        txt = db['data'][k].attrs['txt']
        color=db['data'][k].attrs['text_color']
        font=db['data'][k].attrs['font']

        print('--------------------image:'+str(image_id+1)+'-----------------------')

        viz_textbb(k, rgb, [charBB], wordBB)

        print "image name        : ", colorize(Color.RED, k, bold=True)
        # print "  ** no. of chars : ", colorize(Color.YELLOW, charBB.shape[-1])
        print "  ** no. of words : ", colorize(Color.YELLOW, wordBB.shape[-1])
        print "  ** text         : ", colorize(Color.GREEN, txt)
        print "  ** text_color   : ", colorize(Color.GREEN, color)
        print "  ** font         : ", colorize(Color.GREEN, font)

        height,width = rgb.shape[:2]
        area=height*width

        tmpAnnDicts, global_bbox_id=savejson_textbb(txt, wordBB, global_bbox_id, color, font, area, image_id)

        tmpImDict = {}
        tmpImDict["file_name"] = k.strip('_0')
        tmpImDict['width'] = width
        tmpImDict['id'] = image_id+1
        tmpImDict['height'] = height

        imDicts.append(tmpImDict)
        annDicts += tmpAnnDicts

        # if 'q' in raw_input("next? ('q' to exit) : "):
        #     break

        # if i % 5 == 0:
        #     break
        print('--------------------image:'+str(image_id+1)+' done------------------')

    cateDict = {}
    cateDict['supercategory'] = 'super text'
    cateDict['id'] = 1
    cateDict['name'] = 'text'
    cateDicts.append(cateDict)

    output = {}
    output['images'] = imDicts
    output['annotations'] = annDicts
    output['categories'] = cateDicts

    db.close()

    with open('./results/output.json', 'w')as f:
        json.dump(output, f)

if __name__=='__main__':
    main('results/SynthText.h5')

