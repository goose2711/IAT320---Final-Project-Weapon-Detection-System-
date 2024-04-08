
# IAT320 Final Project (Weapon detecting Alarm System)
#(Programmer: Agastya Oruganti)
#(Designer: Zhaniya Yeltindinova)
#(Project Manager: Jihoon Lee)

import tkinter as tk
from tkinter import ttk
from threading import Thread
from ultralytics import YOLO
import math
import cv2
import datetime
import os
from playsound import playsound  # Uncomment if using playsound for alarm
import threading
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image, ImageTk

# Global variable for the model
model = None

def preload_model():
    global model
    model = YOLO("yolo-Weights/yolov5su.pt")

def play_sound():
    global sound_thread_running
    if not sound_thread_running:
        sound_thread_running = True
        sound = AudioSegment.from_file("alarm.wav")
        play(sound)
        sound_thread_running = False

sound_thread_running = False

def cameraAndDetection():
    global alarmplayed, model
    cap = cv2.VideoCapture(0)
    cap.set(3, 1024)
    cap.set(4, 768)

    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                "teddy bear", "hair drier", "toothbrush", "pistol"
                ]

    # Prepare for recording
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    now = datetime.datetime.now().strftime("%Y-%m-%d%H-%M-%S")
    out = cv2.VideoWriter(f'continuousdetection{now}.avi', fourcc, 20.0, (640, 480))



    blink_red_screen = False

    while True:
        success, img = cap.read()
        if not success:
            break  # Exit if unable to read from the webcam

        results = model(img, stream=True)

        knifedetected = False

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                if classNames[cls] == "knife":
                    knifedetected = True
                    #out.write(img)  # Save the current frame
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                # put box in cam
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # confidence
                    confidence = math.ceil((box.conf[0]*100))/100
                    print("Confidence --->",confidence)

                # class name
                    cls = int(box.cls[0])
                # print("Class name -->", classNames[cls])

                # object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2

                    cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

                    # Blinking red screen effect
                    if knifedetected:
                        if not sound_thread_running:  # Check if sound is not already playing
                            threading.Thread(target=play_sound).start()  # Start playing sound in a new thread

                        if blink_red_screen:
                            overlay = img.copy()
                            overlay[:] = (0, 0, 255)  # Red overlay
                            cv2.addWeighted(overlay, 0.4, img, 0.6, 0, img)
                        blink_red_screen = not blink_red_screen  # Toggle the effect
                    else:
                        blink_red_screen = False  # Reset the effect when no knife is detected 
                    out.write(img)  # Save the current frame                   
                    break

        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def startCamera():
    Thread(target=cameraAndDetection).start()

def createGUI():
    preload_model()
    window = tk.Tk()
    window.title("StealthShield - Home Security Device")
    window.state('zoomed')  # Open the window in maximized state

    # Get the size of the window
    window.update_idletasks()  # Update "requested size" from geometry manager
    width = window.winfo_width()
    height = window.winfo_height()

    # Load the image
    image_path = "C:/Users/gleel/Desktop/IAT320 - Final Project/images/homeScreen.png"
    original_image = Image.open(image_path)
    resized_image = original_image.resize((width, height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)

    # Create a Canvas and add the image to it
    canvas = tk.Canvas(window, width=width, height=height)
    canvas.pack(fill="both", expand=True)
    # Add the image to the canvas
    canvas.create_image(0, 0, image=photo, anchor="nw")

    # Position the button at the bottom of the canvas
    button_y = height - 100  # Adjust this as necessary
    startbutton = ttk.Button(window, text="Start", command=startCamera)
    # Use place to position the button at the bottom
    startbutton.place(x=width/2, y=button_y, anchor="center")

    window.mainloop()

if __name__ == "__main__":
    createGUI()