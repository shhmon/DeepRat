import numpy as np
import cv2
import sys

# x, y, width, height for every video
boundaries = [
	(0, 0, 640, 480),
	(0, 600, 640, 480),
	(1280, 0, 640, 480),
	(1280, 600, 640, 480)
]

np.set_printoptions(threshold=np.inf)

if __name__ == '__main__':

	vid = sys.argv[1]
	cnt = 0

	# Open the video
	cap = cv2.VideoCapture(vid)

	# Some characteristics from the original video
	w_frame, h_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps, frames = cap.get(cv2.CAP_PROP_FPS), cap.get(cv2.CAP_PROP_FRAME_COUNT)

	# output
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	vids = len(boundaries)
	out = []

	for i, bound in enumerate(boundaries):
		out.append(cv2.VideoWriter(f'result{i}.avi', fourcc, fps, (bound[2], bound[3])))

	# Now we start
	while(cap.isOpened()):
		xx = 0 # progress
		ret, frame = cap.read()
		cnt += 1 # Counting frames

		# Make sure there is a frame
		if ret:
			xx = int(cnt*100/frames)
			print(int(xx),'%')

			# Croping the frame
			for i, bound in enumerate(boundaries):
				(x, y, w, h) = bound
				crop_frame = frame[y:y+h, x:x+w]

				# Write frame to output
				out[i].write(crop_frame)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		else:
			break


	cap.release()
	for o in out:
		o.release()
	cv2.destroyAllWindows()