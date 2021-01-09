import scipy.io.wavfile
import numpy as np
import os
import sys
import PySimpleGUI as sg
import webbrowser


def callback(url):
    webbrowser.open_new(url)

def removeTrailingN (dataset):
    cleandata = []
    for i in dataset:
        cleandata.append(i.rstrip("\n"))
    return cleandata

def firstTimeToSeconds (timeline):
    minutes = float(timeline[3:5])
    seconds = float(timeline[6:12])
    actualseconds = (minutes*60) + seconds
    return round(actualseconds, 2)

def secondTimeToSeconds (timeline):
    minutes = float(timeline[20:22])
    seconds = float(timeline[23:29])
    actualseconds = (minutes*60) + seconds
    return round(actualseconds, 2)

def processData (char, wav, captions, folder):

    charname = char
    inputwav = wav
    inputcaptions = captions
    outputfolder = folder
    
    
    data = ""
    timestamps = []
    words = []
    finalpackage = []

    sample_rate, x = scipy.io.wavfile.read(inputwav)

    print(x.shape)
    time = x.shape[0]/sample_rate

    with open(inputcaptions, "r") as f:
        data = f.readlines()
        timestamps = data[1::4]
        for i in range(len(timestamps)):
            timestamps[i] = timestamps[i].replace(",", ".")
        words = data[2::4]

    cleantime = removeTrailingN(timestamps)
    cleanwords = removeTrailingN(words)

    for i in range (0,len(cleantime)):
        finalpackage.append(((firstTimeToSeconds(cleantime[i]),(secondTimeToSeconds(cleantime[i])), cleanwords[i])))

    os.mkdir(outputfolder + "/" + charname +"_AudioFiles") 

    c= open(outputfolder + "/" + charname+".txt","a+")

    for i, audio_data in enumerate(finalpackage):
        #print(audio_data)
        audio_clip = x[int(audio_data[0]*sample_rate) : int(audio_data[1]*sample_rate)]
        scipy.io.wavfile.write(outputfolder+"/"+ charname +"_AudioFiles/"+str(i)+"_"+ charname+"_audio.wav", sample_rate, audio_clip)
        c.write("/"+ charname +"_AudioFiles/"+str(i)+"_"+ charname+"_audio.wav" + "|" + str(audio_data[2] +"\n"))


#------------------------------------
# WINDOW CODE
#------------------------------------

charname = ""
inputwav = ""
inputcaptions = ""
outputfolder = ""

layoutsuccess = [[sg.Text("Processing Complete!")], [sg.Button("Ok")]]

layout = [[sg.Text("Please select an Input Audio File, Caption File, and an Output Location")],     
    
    [
        sg.Text("Character Name (As One Word):"),
        sg.In(size=(25, 1), enable_events=True, key="-CHAR-"),
    ],
    [
        sg.Text("Input Vocal *** .wav **** File (Try https://ontiva.com/en)"),
        sg.In(size=(25, 1), enable_events=True, key="-INPUTWAV-"),
        sg.FileBrowse(file_types=[("Audio File", "*.wav")]),
    ],
    [
        sg.Text("Input .srt Caption File (Try https://downsub.com/)"),
        sg.In(size=(25, 1), enable_events=True, key="-INPUTCAP-"),
        sg.FileBrowse(file_types=(("SRT File", "*.srt"),)),
    ],
    [
        sg.Text("Output Location (Folder)"),
        sg.In(size=(25, 1), enable_events=True, key="-OUTFOLDER-"),
        sg.FolderBrowse(),
    ],

    [sg.Button("Process")]]

# Create the window
window = sg.Window("Voice Parser for 15.ai", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if (event == "Process"):
        char = values['-CHAR-'].rstrip()
        wav = values['-INPUTWAV-'].rstrip()
        captions = values['-INPUTCAP-'].rstrip()
        folder = values['-OUTFOLDER-'].rstrip()
        processData(char, wav, captions, folder)
        successwindow = window = sg.Window("We did it Reddit!", layoutsuccess)

    elif (event =="Ok") or (event == sg.WIN_CLOSED):
        break

window.close()