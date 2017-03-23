from random import gauss
import cv2
import numpy as np
from math import floor

def roundInt(x):
	return int(x + (0.5 if x > 0 else -0.5))

def clip(x, clipval):
	if x > clipval: return clipval
	elif x < -clipval: return -clipval
	else: return x

def brightCal(img, offsetY, offsetX):
	return roundInt(np.sum(img[offsetY:-offsetY,offsetX:-offsetX]))

class image:
	def __init__(self, path):
		self.img = cv2.imread(path)
		self.img = cv2.resize(self.img, (900, roundInt(self.img.shape[0]*900/self.img.shape[1])), interpolation = cv2.INTER_AREA)
		self.H, self.W = self.img.shape[:2]
		self.center = (roundInt(self.H/2), roundInt(self.W/2))
		class component:
			def __init__(self, dragFactor=0.9, springK=0.0001, gaussDev=0.04, offset=40, pos=0):
				self.pos, self.vel, self.acc = 0, 0, 0
				self.dragFactor = dragFactor
				self.springFactor = 0
				self.springK = springK
				self.gaussDev = gaussDev
				self.offset = offset
			def rand(self):
				self.acc = gauss(0, self.gaussDev)
				clip(self.acc, 0.3)
				self.springFactor = -self.springK * self.pos * abs(self.pos)
				self.vel = self.dragFactor * self.vel + self.acc + self.springFactor
				if abs(self.pos + self.vel) < self.offset - 1: self.pos += self.vel
				print 'pos = ', self.pos, 'vel =', self.vel, 'acc =', self.acc
		self.x, self.y = component(), component()
		self.theta = component(springK=0.01,dragFactor=0.5,offset=3, gaussDev=0.025)
		self.maxCenterShift = 10 # maximum no. of pixels through which center of rotation can shift
		self.blur = component(springK=0.01, gaussDev=0.4, offset=2)
		self.bright = brightCal(self.img, self.y.offset, self.x.offset)
		self.brightControl = 0.8 # equalizes the brightness exactly when set to 1
		self.res = (self.img.shape[0]-2*self.y.offset)*(self.img.shape[1]-2*self.x.offset)
		self.first = True

	def centershift(self):
		randY, randX = gauss(0, 0.4*self.maxCenterShift), gauss(0, 0.4*self.maxCenterShift)
		randY, randX = clip(randY, self.maxCenterShift), clip(randX, self.maxCenterShift)
		self.center = (roundInt(self.H/2+randY), roundInt(self.W/2+randX))
		print "center:", self.center

	def view(self, name):
		M = cv2.getRotationMatrix2D(self.center, self.theta.pos, 1.0)
		img2 = cv2.warpAffine(self.img, M, (self.W, self.H))
		brightSum = brightCal(img2, roundInt(self.y.offset-self.y.pos), roundInt(self.x.offset-self.x.pos))
		print 'bright_parameter: f:', brightSum, 'i:', self.bright, 'res:', self.res
		print '\t\t  diff:', brightSum - self.bright, 'param:', (brightSum - self.bright)/self.res, 'control_param:', roundInt(self.brightControl * (brightSum - self.bright)/self.res)
		img2 = cv2.add(img2,np.array([float(roundInt(self.brightControl * (self.bright - brightSum) / self.res))]))
		if self.first:
			self.img3 = img2
			self.first = False
		else: self.img3 = cv2.addWeighted(img2,0.3,self.img3,0.7,0.0)
		blur = 2 * roundInt(abs(self.blur.pos)) + 1
		zoom = roundInt(2 - floor(blur/3))
		print 'blur_pos:', blur, 'zoom_pos:', zoom
		img4 = cv2.GaussianBlur(self.img3,(blur, blur), 0.0)[zoom:-zoom, zoom:-zoom]
		img4 = cv2.resize(img4, (self.W, self.H))
		cv2.imshow(name, img4[roundInt(self.y.offset-self.y.pos):roundInt(-self.y.offset-self.y.pos), roundInt(self.x.offset-self.x.pos):roundInt(-self.x.offset-self.x.pos)])
