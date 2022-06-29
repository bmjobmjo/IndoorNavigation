import requests
import json
from time import sleep, time
import urllib
import json
import traceback
import urllib.request
from PIL import Image
import math
centerX=650
centerY=480
alpha = ""
topX= 0
leftY= 0
current_loc_index = int(0)  # index loction in route array
route1 = {"A", "WE", "C", "D", "E"}

def http_connect():
    x = requests.get('http://192.168.141.76/L')
    sleep(200)
    x = requests.get('http://192.168.141.76/L')
    sleep(200)
    x = requests.get('http://192.168.141.76/L')
def ocr_space_file(filename, overlay=True, api_key='K87189462688957', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """
    print("here in def");
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'OCREngine': 2,
               'scale': True,

               'detectOrientation': True
               }
    with open(filename, 'rb') as f:
        try:
            r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            print("Time out")
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            print("toomany redirect")
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            print("request expception")

    return r.content.decode()



#print("starting");
# Use examples:
def captureimage():
    urllib.request.urlretrieve(
        'http://192.168.148.192/capture',
        "gfg.jpeg")
    print("here 1");
    img = Image.open("gfg.jpeg")
    img.show()
    print("here  image show")
    return 0


def parse(json_out, textToFound):
    dict_json = json.loads(json_out)
    print("parse alpahbet deteted res...")

    l = int(0)
    w = int(0)
    found = bool(False)
    alpha = str("")
    while True:
        w = 0
        while True:
            try:
                alpha = dict_json['ParsedResults'][0]['TextOverlay']['Lines'][l]['Words'][w]['WordText']
            except:
                print("not found words")
                break  # index out of range  break the loop and check next line

            if alpha == textToFound:
                print(alpha)
                print("parse left res...")
                print(dict_json['ParsedResults'][0]['TextOverlay']['Lines'][0]['Words'][0]['Left'])
                leftX = dict_json['ParsedResults'][0]['TextOverlay']['Lines'][0]['Words'][0]['Left']
                print("parse top res...")
                print(dict_json['ParsedResults'][0]['TextOverlay']['Lines'][0]['Words'][0]['Top'])
                topY = dict_json['ParsedResults'][0]['TextOverlay']['Lines'][0]['Words'][0]['Top']
                print("parse height res...")
                print(dict_json['ParsedResults'][0]['TextOverlay']['Lines'][0]['Words'][0]['Height'])
                height = dict_json['ParsedResults'][0]['TextOverlay']['Lines'][0]['Words'][0]['Height']
                print("parse Width res...")
                print(dict_json['ParsedResults'][0]['TextOverlay']['Lines'][0]['Words'][0]['Width'])
                width = dict_json['ParsedResults'][0]['TextOverlay']['Lines'][0]['Words'][0]['Width']
                found = True
                break  # found so break the loop
            w += 1
        l += 1
        if found:
            break # found so break the loop
        if l > 3:
            break
    return  found



def route_find(alpha):

    for x in route1:
        if alpha == x:
            if x != previous:
                print("in route ")
                previous = x
                # call function to centre under it
    return 0


def center_it(left,top,centerX,centerY):
    x=left-centerX;
    y=top-centerY;
    tetha= math.degrees(math.atan(x/y))
    print("thetha =")
    print(tetha)
    if (tetha>10)&(tetha<175):
        #turn left
       # x = requests.get('http://192.168.141.76/L')
        print("moving left ")
    else:
        # x = requests.get('http://192.168.141.76/R')
        print("moving right ")
    if (tetha<10)&(tetha>350):
        # x = requests.get('http://192.168.141.76/F')
        print("moving forward ")
    return 0

def move_to_current_route_marker(json_text):

    text_to_found = route1[current_loc_index]
    if parse(json_text, text_to_found):
        center_it(leftX, topY, centerX, centerY)



#main
#http_connect()
while 1:
    captureimage()
    json_out = ocr_space_file(filename="D:\\Downloads\\gfg.jpeg", language='pol')

    #test_file = ocr_space_file(filename='C:\\Users\\ACER\\Documents\\java\\jonfp.txt', language='pol')
    #test_file=open("C:\\Users\\ACER\\Documents\\java\\jonfp.txt")

    #filejson = open('D:\\BMJO\\jsonres.json')
    #json_out = filejson.read()
    move_to_current_route_marker(json_out)
    print("here")
    print(json_out)