from lib.GoProCapture import GoProCapture
import zmq, json, cv2
from lib.utils import image_to_string, undistort
import time, base64
from imutils.video import WebcamVideoStream

import socket, struct, pickle


SERVER_ADDRESS = "35.163.137.148"
# SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = '5555'
GOPRO_URL = "udp://127.0.0.1:2000"

CAPTURE_CALIBRATION_DATA = False
USE_GOPRO = False
USE_RASPBERRY_PI = False

if USE_GOPRO:
	captureProc = GoProCapture(GOPRO_URL)
	captureProc.start()

context = zmq.Context(4)
footage_socket = context.socket(zmq.PAIR)
footage_socket.connect('tcp://' + SERVER_ADDRESS + ':' + SERVER_PORT)

#clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#clientsocket.connect((SERVER_ADDRESS,SERVER_PORT))

time.sleep(1) 
if(USE_GOPRO):
	cap = cv2.VideoCapture(GOPRO_URL)
elif(USE_RASPBERRY_PI):
	cap = VideoStream(usePiCamera=True,
						 resolution=(1280,720),
						 framerate=30).start()
else:
	# cap = WebcamVideoStream(src=0).start()
	cap = cv2.VideoCapture('udp://0.0.0.0:8080')
	# cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
	# cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
	# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
	# cap.set(cv2.IMWRITE_JPEG_QUALITY, 10)

count = 0
print("Started WebStream")
t = time.time()
while True: 
	ret, frame = cap.read()
	if frame is not None:
		count = count + 1
		# print(frame.shape)

		if CAPTURE_CALIBRATION_DATA:
			if count % 5 == 0:
				cv.imwrite("./calibration_frames/frame%d.jpg" % count, frame)
		else:
			# undistortedFrame = undistort(frame)
			timestamp = int(round(time.time() * 1000))
			frameString = image_to_string(frame)
			# # frameString = base64.b64encode(frame)

			frameDict = {
				'frameString': frameString.decode('ascii'),
				'timestamp': timestamp
			}
			# frameDictJSON = json.dumps(frameDict)
			# clientsocket.sendall(struct.pack("L", len(frameDictJSON))+frameDictJSON)
			# data = pickle.dumps(frame)
			# frameString = image_to_string(frame)
			# clientsocket.sendall(struct.pack("L", len(data))+data) ### new code

			footage_socket.send_json(frameDict)

			fps = count/(time.time()-t)
			print("fps: {}".format(fps))


