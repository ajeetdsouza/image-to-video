#!/usr/bin/python

from cv2 import destroyAllWindows, waitKey
import fn
from sys import argv
from os.path import isfile

if __name__ == '__main__':
	if len(argv) != 2:
		print "invalid syntax. use 'python augment.py image.jpg'"
		exit(0)
	if not isfile(argv[1]):
		print "file not found. use 'python augment.py image.jpg'"
		exit(0)
	img = fn.image(argv[1])
	while(True):
		img.view('output')
		k = waitKey(1)
		if k == ord('q'):
			destroyAllWindows()
			break
		img.centershift()
		print 'theta:',
		img.theta.rand()
		print 'x:',
		img.x.rand()
		print 'y:',
		img.y.rand()
		img.blur.rand()
		print '\n'
