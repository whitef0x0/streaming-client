from multiprocessing import Process
from goprocam import GoProCamera
from goprocam import constants
import zmq, json, cv2
from lib.utils import image_to_string
import time

# distributes data and spawns sub processes
class GoProCapture(Process):
	def __init__(self, gopro_url):
		self.gopro = GoProCamera.GoPro()
		self.gopro_url = gopro_url
		super(GoProCapture, self).__init__()

	def run(self):
		self.gopro.stream(self.gopro_url)


