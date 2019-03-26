from lib.GoProCapture import GoProCapture
import zmq, json, cv2
from lib.utils import image_to_string, undistort
import time

SERVER_ADDRESS = "18.237.234.155"
#SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = "5555"
GOPRO_URL = "udp://127.0.0.1:2000"

CAPTURE_CALIBRATION_DATA = False
USE_GOPRO = False
USE_RASPBERRY_PI = False

if USE_GOPRO:
	captureProc = GoProCapture(GOPRO_URL)
	captureProc.start()

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://' + SERVER_ADDRESS + ':' + SERVER_PORT)

time.sleep(1) 
if(USE_GOPRO):
	cap = cv2.VideoCapture(GOPRO_URL)
elif(USE_RASPBERRY_PI):
	cap = VideoStream(usePiCamera=True,
                         resolution=(1280,720),
                         framerate=30).start()
else:
	cap = cv2.VideoCapture(0)

count = 0
print("Started WebStream")
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

			frameDict = {
				'frameString': frameString.decode('ascii'),
				'timestamp': timestamp
			}
			frameDictJSON = json.dumps(frameDict)

			footage_socket.send_string(frameDictJSON)


