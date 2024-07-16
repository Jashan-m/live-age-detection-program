import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
AGE_GROUPS = [(0, 2), (4, 6), (8, 12), (15, 20), (25, 32), (38, 43), (48, 53), (60, 100)]
AGE_LABELS = ["0-2", "4-6", "8-12", "15-20", "25-32", "38-43", "48-53", "60+"]
def detect_age(face_img):
    face_area = face_img.shape[0] * face_img.shape[1]
    if face_area < 5000: 
        return "0-2"
    elif face_area < 10000:
        return "4-6"
    elif face_area < 20000:
        return "8-12"
    elif face_area < 30000:
        return "15-20"
    elif face_area < 40000:
        return "25-32"
    elif face_area < 50000:
        return "38-43"
    elif face_area < 60000:
        return "48-53"
    else:
        return "60+"
def update_video_feed():
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            age_label = detect_age(face_img)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, f'Age: {age_label}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.img_tk = img_tk
    root.after(10, update_video_feed)
root = tk.Tk()
root.title("Live Age Detection")
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()
start_button = ttk.Button(root, text="Start Age Detection", command=update_video_feed)
start_button.pack()
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
root.mainloop()
cap.release()
cv2.destroyAllWindows()
