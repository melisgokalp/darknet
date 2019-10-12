
print("DKF")
import zmq
print("DKF2")
import os
import darknet
print("DKF3")
import sys
import time
print("DKFcheckcv")
print("DKF4")
import struct
print("DKF5")
import numpy as np

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

#import the library wrappers
import lib.vprosthesis_pb2 as vprosthesis_pb2
from lib.ports import FRAME_PORT
from lib.sockets import create_publisher
from lib.topics import FRAME_TOPIC, SEP

#context = zmq.Context()
#framechange_socket = create_publisher(context, FRAME_PORT) #publisher socket
#frame_socket = create_subscriber(context, FRAME_PORT, "".encode("utf-8"), queue_messages=False)
#fetch_frame() #fetch images as a subscriber

TIMESTAMP_BYTES = 8

def fetch_frame():
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    while (True):
        img = getRGBFrame()
        cv2.imshow('frame', img) #no need but keep for sanity check
        detections = darknet.performDetect()
        if cv2.waitKey(1) == 27:
            break # esc to quit
    cv2.destroyAllWindows()
    
def getRGBFrame():
    frame_data = frame_socket.recv()
    buf = bytes(frame_data)
    array1D = np.frombuffer(buf[TIMESTAMP_BYTES:], dtype=np.uint8)
    img = np.reshape(array1D, (720, 1280, 3), order='C')
    timestamp = struct.unpack('Q', buf[0:TIMESTAMP_BYTES])[0]
    return img, timestamp

def convert_msg(detections):
    return None

def publish_probs(msg):
	framechange_socket.send(FRAME_TOPIC + SEP + msg)
    
detections = darknet.performDetect()
print(detections)

def main():
	#pull frames from the camera using cv
	#darknet.performdetect on cam image
	fetch_frame()
	#



