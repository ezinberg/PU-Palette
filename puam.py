# puam.py
# get images from pu art museum site through iiif protocol

import urllib, json
import requests
import pprint
from PIL import Image
import wget

import time



def test():

    total_time = 0
    for a in range(0,3):

        start = a * 10000
        end = start + 100

        start_time = time.time()
        for i in range(start,end):
            # object = 
            

            url = "https://data.artmuseum.princeton.edu/objects/" + str(i)

            r = requests.get(url)

            

            if r.status_code == 200:
                # pprint.pprint(r.json()) 
                json = r.json()
                titlelist = json["titles"]
                if len(titlelist) > 0:
                    title = titlelist[0]["title"]
                    # print(title)

                medialist = json["media"]
                if len(medialist) > 0:
                    for j in range(0, len(medialist)):
                        imglink = medialist[j]["uri"]
                        # print(imglink)

        end_time = time.time()
        run_time = end_time - start_time  
        print(run_time)
        total_time = total_time + run_time

    avg_time = total_time / 300

    print("avg = " + str(avg_time))


def showTitles(start, end):

    for i in range(start,end):

            url = "https://data.artmuseum.princeton.edu/objects/" + str(i)

            r = requests.get(url)

            if r.status_code == 200:
                # pprint.pprint(r.json()) 
                json = r.json()
                titlelist = json["titles"]
                if len(titlelist) > 0:
                    title = titlelist[0]["title"]
                    print(title)

                medialist = json["media"]
                if len(medialist) > 0:
                    for j in range(0, len(medialist)):
                        imglink = medialist[j]["uri"]
                        # print(imglink)

def showImages(start, end):
    for i in range(start,end):

            url = "https://data.artmuseum.princeton.edu/objects/" + str(i)

            r = requests.get(url)

            if r.status_code == 200:
                # pprint.pprint(r.json()) 
                json = r.json()
                titlelist = json["titles"]
                if len(titlelist) > 0:
                    title = titlelist[0]["title"]
                    print(title)

                medialist = json["media"]
                if len(medialist) > 0:
                    for j in range(0, len(medialist)):
                        imglink = medialist[j]["uri"]

                        # modified = imglink[:-4]
                        modified = imglink + "/full/full/0/default.jpg"
                        print(modified)

                        # rImg = requests.get(imglink)
                        # # pprint.pprint(rImg.json()) 

                        # im = Image.open(rImg)
                        # im.show()

                        image_filename = wget.download(modified)
                        print(image_filename)
                        im = Image.open(image_filename)
                        im.show()


def main():

    # TEST_FOR_TIME = False

    # if TEST_FOR_TIME:
    #     test()


    # else:
    #     showTitles(20000,20100)

    showImages(20000,20100)





main()