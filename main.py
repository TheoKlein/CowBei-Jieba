# -*- coding: utf-8 -*-
from pathlib import Path
from wordcloud import WordCloud
from PIL import Image
import argparse
import requests
import pandas as pd 
import csv
import jieba
import jieba.posseg as pseg
import numpy as np
import shutil
import os
import sys

# Get your token from Facebook Graph API https://developers.facebook.com/tools/explorer
FACEBOOK_TOKEN = ''

# default filename
FILENAME = 'CowBei'

def collectPagePosts():
    """
    Get posts from Facebook graph API.
    """
    # All page you want to grab
    fanpage = {
        # 'Page ID number or ID string': 'Custom Page Name'
        '576881715763166': '靠北輔大'
    } 

    if(os.path.isdir('tmp')):
        shutil.rmtree('tmp')
    os.makedirs('tmp')

    for ele in fanpage:
        # set FACEBOOK_TOKEN and filename to current page name
        global FACEBOOK_TOKEN
        global FILENAME
        FILENAME = fanpage[ele]

        while True:
            FACEBOOK_TOKEN = input(
    """To make sure token will not expired during the process,
you will need to enter the token at the begin of every pages.\n
You can get the token from here: https://developers.facebook.com/tools/explorer\n
Token: """
            )

            try:
                res = requests.get('https://graph.facebook.com/v2.10/{}/posts?limit=100&access_token={}'.format(ele, FACEBOOK_TOKEN))

                if 'error' in res.json():
                    raise Exception(res.json()['error']['message'])
            except Exception as e:
                print('\n[Error] {}\n'.format(e))
            else:
                break

        print('Grabing {}\'s posts. This may take a lot of time!'.format(fanpage[ele]))
        
        information_list = []
        while 'paging' in res.json(): 
            print('.', end='', flush=True)
            for information in res.json()['data']:
                if 'message' in information:
                    information_list.append([
                        "\"{}\"".format(fanpage[ele]),
                        "\"{}\"".format(' '.join(information['message'].split("\n")))
                    ])

            # Go to next page if exist
            if 'next' in res.json()['paging']:
                res = requests.get(res.json()['paging']['next'])
            else:
                break
        print('\n')

        file = Path('tmp/{}.csv'.format(FILENAME))
        if file.is_file():
            print('Remove the older file.')
            os.remove('tmp/{}.csv'.format(FILENAME))
            
        # Write to csv file
        information_df = pd.DataFrame(information_list, columns=['Page', 'Message']) 
        information_df.to_csv("tmp/{}.csv".format(FILENAME) , index=False) 
        analyze()

def analyze():
    """
    Get posts from csv file and use Jieba to cut and collect words.
    """
    jieba.set_dictionary('data/CHT_dict.txt') 
    #jieba.set_dictionary('data/custom_dict.txt') 

    hash = {}
    ignore_words = []
    ignore_flag = ["x", "m", "eng"]

    with open("data/ignore_dict.txt") as f:
        ignore_words = f.readlines()
    ignore_words = [x.strip() for x in ignore_words] 

    # Process csv file
    print("Start analyzing the csv file. This may take a lot of time!\n")
    f = open("tmp/{}.csv".format(FILENAME), 'r')
    posts = len(list(open("tmp/{}.csv".format(FILENAME), 'r')))
    progress = 0
    for row in csv.DictReader(f):
        d = pseg.cut(row['Message'])
        for word, flag in d:
            if flag not in ignore_flag and word not in ignore_words:
                if word in hash:
                    hash[word] += 1
                else:
                    hash[word] = 1
        progress += 1
        print('\rAnalyzing {}: {}/{} posts'.format(FILENAME, progress, posts), end='', flush=True)
    f.close()
    print('')

    fd = open("tmp/{}-count.csv".format(FILENAME), "w")
    fd.write("word,count\n")
    for k in hash:
        fd.write("%s,%d\n" % (k,hash[k]))
    fd.close()

    wordcloud()

def wordcloud():
    """
    Generate the wordcloud.
    """
    print('Creating wordcloud file: {}.png\n'.format(FILENAME))
    text = csv.reader(open('tmp/{}-count.csv'.format(FILENAME), 'r',newline='\n'))
    next(text, None)

    d = {}

    f = open('tmp/{}-count.csv'.format(FILENAME), 'r')
    for row in csv.DictReader(f):
        d[row['word']] = float(row['count']) 

    wordcloud = WordCloud(
        width=2000,
        height=1000,
        max_words=400,
        font_path="data/cwTeXHei-zhonly.ttf",
        background_color='white'
    ).generate_from_frequencies(d) 
    
    image = wordcloud.to_image()
    image.save('tmp/{}.png'.format(FILENAME))

if __name__ == '__main__':
    collectPagePosts()