# image-to-video

A little script I wrote in Python 2.7 and OpenCV 3 to make a still image appear like a video recording.

The aim of the program is to keep the output reasonably realistic while also performing data augmentation to get a seemingly limitless video feed.

## Features
- Randomized image panning
- Randomized image rotation
- Occasional defocusing with slight zoom (note that true bokeh blurring is technically impossible to simulate, but Gaussian blurring is a decent approximation of it, so I've used that instead)
- White balance (brightness adjusts as the image moves)
- Motion blurring (again, a very rough implementation, since a realistic one is hard to simulate with just a single image)
- All of these are parametized, so it's very easy to tweak the output to your liking. I haven't experimented with the parameters much myself, but you should be able to get a pretty realistic output.

## Demo
[Sample video](https://www.youtube.com/watch?v=XiauKmGAaBc)
This example shows the program in action with a ROS wrapper that takes a picture from the webcam (using [cv_camera](http://wiki.ros.org/cv_camera), not shown in the video) and displays a video output.

## Requirements
- [OpenCV](http://opencv.org/)
- [NumPy](http://www.numpy.org/)

## Usage
Pretty straightforward. Pass the file name as a parameter.
`python augment.py filename.jpg`
