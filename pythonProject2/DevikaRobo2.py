import playsound as playsound
import requests
import json
from time import sleep, time
import urllib
import json
import traceback
import urllib.request
from PIL import Image as Image2
import math
from tkinter import *
from tkinter import messagebox
from gtts import gTTS
from playsound import playsound
import pyttsx3

centerX = 160
centerY = 120
alpha = ""
topX = int(0)
leftY = int(0)
leftX = int(0)
topY = int(0)
current_loc_index = int(0)  # index loction in route array
route1 = {"BI", "WE", "C", "D", "E"}
webServURL = "http://192.168.45.58/"
cameraURL = "http://192.168.45.192/"


def http_connect():
    x = requests.get('http://192.168.148.58/F')
    sleep(200)
    x = requests.get('http://192.168.141.58/L')
    sleep(200)
    x = requests.get('http://192.168.141.58/L')


def move_forward(steps):
        x = requests.get(webServURL + steps)


def move_back(steps):
        x = requests.get(webServURL + steps)



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
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


# print("starting");
# Use examples:
def captureimage():
    camURLTem = cameraURL + "capture"
    urllib.request.urlretrieve(
        camURLTem,
        "gfg.jpeg")
    print("here 1");
    # img = Image2.open("gfg.jpeg")
    # img.show()
    # print("here  image show")
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
                print("left =")
                print(dict_json['ParsedResults'][0]['TextOverlay']['Lines'][0]['Words'][0]['Left'])
                leftX = dict_json['ParsedResults'][0]['TextOverlay']['Lines'][0]['Words'][0]['Left']
                print("top = ")
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
            center_it(leftX, topY, centerX, centerY)
            break  # found so break the loop
        if l > 3:
            break
    return found


def route_find(alpha):
    for x in route1:
        if alpha == x:
            if x != previous:
                print("in route ")
                previous = x
                # call function to centre under it
    return 0

dist_inc_count = int(0);
last_dist = float(10000.0)

def center_it(top, left, centerX, centerY):
    x = centerX - left
    #if(abslast_dist)
    g = float("{:.2f}".format(x))

    move_step_f = "F"
    move_step_b = "B"
    if abs(x) >= 40:
        play_audio("Target is located at " + str(g) + " away now - Moving fast")
        move_step_f = "FFF"
        move_step_b = "BBB"
    elif abs(x) >= 20:
        play_audio("Target is located at " + str(g) + " away now - Moving fast")
        move_step_f = "FF"
        move_step_b = "BB"
    elif abs(x) >= 10:
        play_audio("Target is located at " + str(g) + " away now - Fine adjust Location")
        move_step_f = "F"
        move_step_b = "B"

    if x > 10.0:

        move_back(move_step_f)
        print("moving back")
    elif x < -10.0:
        move_forward(move_step_b)
        print("moving back")
    else:
        play_audio("Target in limits - no movement needed")
        mesg = "Left =" + str(left) + " Top=" + str(top) + " Disp=" + str(x);
        # messagebox.showinfo("Robo", mesg)

    return 0


def move_to_current_route_marker(json_text):
    text_to_found = "A"
    parse(json_text, text_to_found)



def play_audio2(message):
    try:
        language = 'en'
        myobj = gTTS(text=message, lang=language, slow=False)
        myobj.save('welcome.mp3')
        playsound('welcome.mp3')
    except:
        print("audio error")


engine = pyttsx3.init()
voices = engine.getProperty('voices')  # getting details of current voice
# engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female


def play_audio(message):
    engine.say(message)
    engine.runAndWait()


play_audio("Devika's limbing robot welcomes you")
while 1:
    # from cam
    print("image capturing")
    # messagebox.showinfo("Robo", "image capturing")
    play_audio("Capturing Image")
    captureimage()
    print("Captured image")
    play_audio("Sending Image to OCR to locate route")
    json_out = ocr_space_file(filename='gfg.jpeg', language='pol')
    print("OCR complete")
    print("Prints the json from the save file")
    print(json_out)
    print("Process and move")
    play_audio("Parsing OCR Text")
    move_to_current_route_marker(json_out)
    ##print("Prints the json from ocr ")
    # print(test_file)

    # print(test_file)
    # from file
    # file = open('json.txt', 'w')
    # file.write(test_file)
    # file.close()
    # test_file = open("json.txt")
    # json_out = test_file.read()
    # move_to_current_route_marker(json_out)
