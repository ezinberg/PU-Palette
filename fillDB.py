# fillDB.py
# creates and populates SQL db

import sqlite3
import urllib, json
import requests
import pprint
# https://www.geeksforgeeks.org/python-pil-image-show-method/
from PIL import Image
import wget
import time


def createTable(c):

    # create OBJECTS table
    c.execute('''CREATE TABLE OBJECTS(
                    ID             INT PRIMARY KEY     NOT NULL,
                    TITLE          TEXT                NOT NULL,
                    ARTIST         TEXT                NOT NULL,
                    COUNTRY        TEXT,
                    DISPLAYDATE    TEXT,
                    DATE           DATE,
                    IMAGE          BLOB,
                    COLOR1R        INT,
                    COLOR1G        INT,
                    COLOR1B        INT,
                    COLOR2R        INT,
                    COLOR2G        INT,
                    COLOR2B        INT,
                    COLOR3R        INT,
                    COLOR3G        INT,
                    COLOR3B        INT,
                    COLOR4R        INT,
                    COLOR4G        INT,
                    COLOR4B        INT,
                    COLOR5R        INT,
                    COLOR5G        INT,
                    COLOR5B        INT
                    )''')


# https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/
def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

# https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/
def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

# https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/
def readBlobData(empId):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from new_employee where id = ?"""
        cursor.execute(sql_fetch_blob_query, (empId,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1])
            name  = row[1]
            photo = row[2]
            resumeFile = row[3]

            print("Storing employee image and resume on disk \n")
            photoPath = "E:\pynative\Python\photos\db_data\\" + name + ".jpg"
            resumePath = "E:\pynative\Python\photos\db_data\\" + name + "_resume.txt"
            writeTofile(photo, photoPath)
            writeTofile(resumeFile, resumePath)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")


# testing image retreival and display from db
def testOpenImage(id):
    conn = sqlite3.connect('puam.db')
    c = conn.cursor()

    # query = '''INSERT INTO OBJECTS(ID,TITLE,ARTIST,COUNTRY,DISPLAYDATE,DATE,IMAGE) 
                            # VALUES (?,?,?,?,?,?,?)'''

    query = "SELECT IMAGE FROM OBJECTS WHERE ID=?"
    
    # cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
    value = (id,)
    c.execute(query, value)
    imageBinary = c.fetchall()[0][0]

    # print(imageBinary)

    print("Storing image on disk \n")
    photoPath = "./images/" + str(id) + ".jpg"
    writeTofile(imageBinary, photoPath)
    conn.close()




def main():
    # initialize connection and cursor
    conn = sqlite3.connect('puam.db')
    c = conn.cursor()

    # createTable(c)

    TOTAL_ARTIFACTS = 54183

    start = time.time()

    # insert all possible IDs into table
    for i in range(49850, TOTAL_ARTIFACTS):

        # print status
        if i % 100 == 0:
            print("\n" + str(i))
            print("progress: " + str(int(100*i/TOTAL_ARTIFACTS)) + "%")
            print("time elapsed: " + str(int((time.time()-start)/60)) + " minutes")


        id = i
        title = ""
        artist = ""
        country = ""
        displayDate = ""
        date = ""
        image = ""

        url = "https://data.artmuseum.princeton.edu/objects/" + str(id)

        r = requests.get(url)

        if r.status_code == 404:
            continue

        if r.status_code == 200:
            json = r.json()

            titlelist = json["titles"]
            if len(titlelist) > 0:
                title = titlelist[0]["title"]
            
            if title == "":
                continue
            
            makerslist = json["makers"]
            if len(makerslist) > 0:
                artist = makerslist[0]["displayname"]

            geographylist = json["geography"]
            if len(geographylist) > 0:
                country = geographylist[0]["country"]
            
            if country == "":
                continue

            if "displaydate" in json.keys():
                displayDate = json["displaydate"]

            date = json["datebegin"]

            medialist = json["media"]
            if len(medialist) > 0:
                imglink = medialist[0]["uri"]
                # https://iiif.io/api/image/2.1/#size
                modified = imglink + "/full/full/0/default.jpg"

                if requests.get(modified).status_code != 200:
                    continue

                image_filename = wget.download(modified)
                image = convertToBinaryData(image_filename)

            if image == "":
                continue


            values = (id, title, artist, country, displayDate, date, image)

            query = '''INSERT INTO OBJECTS(ID,TITLE,ARTIST,COUNTRY,DISPLAYDATE,DATE,IMAGE) 
                            VALUES (?,?,?,?,?,?,?)'''
            
            c.execute(query, values)
            conn.commit()
        
    conn.commit()
    conn.close()

    # id = 24444
    # testOpenImage(id)
    # im = Image.open("./images/" + str(id) + ".jpg")
    # im.show()



main()
