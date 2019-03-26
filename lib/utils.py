import numpy as np
import cv2

def image_to_string(image):
	import cv2
	import base64
	encoded, buffer = cv2.imencode('.jpg', image)
	return base64.b64encode(buffer)


def string_to_image(string):
	import numpy as np
	import cv2
	import base64
	frame = base64.b64decode(string.encode('ascii'))
	npframe = np.fromstring(frame, dtype=np.uint8)
	return cv2.imdecode(npframe, 1)

# You should replace these 3 lines with the output in calibration step
DIM=(432, 240)
K=np.array([[199.21276417545496, 0.0, 221.3465905005841], [0.0, 196.9983201034311, 112.5303530483567], [0.0, 0.0, 1.0]])
D=np.array([[0.06646854014891504], [-0.21684147450428695], [0.8391311375496778], [-0.8826261877468958]])

def undistort(frame, balance=0.0, dim2=None, dim3=None):

    dim1 = frame.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort

    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"

    if not dim2:
        dim2 = dim1

    if not dim3:
        dim3 = dim1

    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0

    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    return undistorted_frame