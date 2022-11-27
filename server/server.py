import socket
# import base64
# import time
# import imutils
# import cv2
# import numpy as np


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IP, SOCK_STREAM = TCP
server.bind(('', 1002))  # 127.0.0.1
server.listen()

client_socket, client_address = server.accept()

file = open('./temp_for_program/server_image.png', "wb")
image_chunk = client_socket.recv(16384)  # stream-based protocol

while image_chunk:
    file.write(image_chunk)
    image_chunk = client_socket.recv(16384)

file.close()
client_socket.close()

print('server off')
