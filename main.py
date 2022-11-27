from colorama import Fore, Back, Style
import PySimpleGUI as sg
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from sys import platform
import base64
import imutils
import os
import socket
import struct
import cv2
import numpy as np
import time

num = ""
s = socket.socket
BUFF_SIZE = 65536


def main():
    # os.system("cd C: && mkdir temp_for_program")
    if os.path.exists('temp_for_program'):
        pass
    else:
        os.mkdir("temp_for_program")

    UI()  # основная программа


def send_to_analize():
    pass


def UI():
    layout = [[sg.Text("Выберите файл")],
              [sg.Button('Открыть фото файл', key=("OPEN_FILE")), sg.Text(num, key='FILE')],
              [sg.Button('Открыть видео файл', key=("OPEN_VIDEO")), sg.Text(num, key='VIDEO')]],
    window = sg.Window('Neuro Link', layout)
    event, values = window.read()

    if event == "OPEN_FILE":
        print("OKey")
        file_link = select_file()
        print(Fore.GREEN + file_link)

        send_file(filename=file_link)

    elif event == "OPEN_VIDEO":
        print("Video")
        file_link = select_file()
        print(Fore.RED + file_link)

        # send_to_analize()



    else:
        print("Not found...")


def select_file():
    Tk().withdraw()
    filename = askopenfilename()
    print(f'Вы выбрали файл - {filename}')
    return filename


def send_file(filename):
    HOST = '127.0.0.1'  # '127.0.0.1'
    PORT = 1002
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
    client.connect((HOST, PORT))  # 127.0.0.1
    print(filename)

    file = open(filename, 'rb')
    image_data = file.read(16384)
    while image_data:
        client.send(image_data)
        image_data = file.read(16384)
    print('end')

    file.close()
    client.close()


def send_video(filename):
    print("test")

    print("video")
    HOST = socket.gethostname()
    PORT = 9999
    BUFF_SIZE = 65536

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    socket_address = (HOST, PORT)
    server_socket.bind(socket_address)
    print('Listening at:', socket_address)

    vid = cv2.VideoCapture(filename)  # replace 'rocket.mp4' with 0 for webcam
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)

    while True:
        msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ', client_addr)
        WIDTH = 360
        while (vid.isOpened()):
            _, frame = vid.read()
            frame = imutils.resize(frame, width=WIDTH)
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            message = base64.b64encode(buffer)
            server_socket.sendto(message, client_addr)
            frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                server_socket.close()
                break
            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count / (time.time() - st))
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt += 1


def get_system():
    if platform == "linux" or platform == "linux2":
        print("linux")
        system = "linux"
        return system
    elif platform == "darwin":
        print("macos")
        system = "mac"
        return system
    elif platform == "win32":
        print("win")
        system = "windows"
        return system
    else:
        print("Система не найдена")
        return "Error"


# start
main()
