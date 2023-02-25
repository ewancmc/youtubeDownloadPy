import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
from pytube import YouTube
from pytube.cli import on_progress
import os

def Widgets():
    tk.Entry(fg="blue", bg="white", width=50, textvariable=urlEntry).pack()
    tk.Button(text="Submit URL", width=25, command=DownloadThread).pack()
    #ttk.Progressbar(window, orient="horizontal", length=100, mode='determinate', variable=downloadProgress).pack()
    #tk.Label(window, text='', variable=progressLabel).pack()




def DownloadAudio():
    url = urlEntry.get()
    
    if urlEntry == '':
        showerror(title='Error', message='Please enter the YouTube URL')
    else:
        try:
            def OnProgress(stream, chunk, bytesRemaining):
                # the total size of the audio
                totalSize = stream.filesize
                # this function will get the size of the audio file
                def GetFormattedSize(totalSize, factor=1024, suffix='B'):
                    # looping through the units
                    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                        if totalSize < factor:
                            return f"{totalSize:.2f}{unit}{suffix}"
                        totalSize /= factor
                    # returning the formatted audio file size
                    return f"{totalSize:.2f}Y{suffix}"
                    
                # getting the formatted audio file size calling the function
                formattedSize = GetFormattedSize(totalSize)

                # the size downloaded after the start
                bytesDownloaded = totalSize - bytesRemaining

                # the percentage downloaded after the start
                percentageCompleted = round(bytesDownloaded / totalSize * 100)

                # updating the progress bar value
                downloadProgress['value'] = percentageCompleted

                # updating the empty label with the percentage value
                #progressLabel.config(text=str(percentageCompleted) + '%, File size:' + formattedSize)

                # updating the main window of the app
                window.update()
            
            audio = YouTube(url, on_progress_callback=OnProgress)
            outputAudio = audio.streams.get_audio_only().download()
            base, ext = os.path.splitext(outputAudio)
            newFile = base + '.mp3'
            os.rename(outputAudio, newFile)
            print("Audio downloaded")

        except:
            showerror(title='Download Error', message='An error occurred while trying to ' \
                    'download the MP3\nThe following could ' \
                    'be the causes:\n->Invalid link\n->No internet connection\n'\
                     'Make sure you have stable internet connection and the MP3 link is valid')
                # ressetting the progress bar and the progress label
            downloadProgress['value'] = 0

def DownloadThread():
    t1 = threading.Thread(target=DownloadAudio)
    t1.start()   
            
    

    
    
    

#def progress_function(stream=None, chunk=None, file_handle=None, remaining=None):
#    percent = (100 * (fileSizeInBytes - remaining)) / fileSizeInBytes
#    print("{:00.0f}% downloaded".format(percent))
    

window = tk.Tk()
window.title("YouTube Downloader")

urlEntry = StringVar()

Widgets()

downloadProgress = ttk.Progressbar(window, orient="horizontal", length=100, mode='determinate')
downloadProgress.pack()

window.mainloop()

