## Project 4 Writeup 

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./Images/writeup_images/calibrationexample.jpg "Undistorted"
[image2]: ./Images/writeup_images/undistort.jpg "Road Transformed"
[image3]: ./Images/writeup_images/threshold.jpg "Binary Example"
[image4]: ./Images/writeup_images/warped.jpg "Warp Example"
[image5]: ./Images/writeup_images/Fit_Visual.jpg "Fit Visual"
[image6]: ./Images/writeup_images/Output.jpg "Output"
[video1]: ./project_video_solution.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the IPython notebook located in "./Calibration.ipynb" 

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 


![Undistorted][image1]

###  Pipeline (single images)

####  1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:

![Distortion Test][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image (thresholding steps in function `threshold_pipeline` in notebook `Final_Pipeline.ipynb`).  Here's an example of my output for this step. 

![Binary Image][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warp()`, which appears in  `Final_Pipeline.ipynb`.  The `warp()` function takes as inputs an image (`img`). I chose to hardcode the source and destination points in the following manner:

```python
source_pts = np.array([ [0 + 175, dst.shape[0]], [590, 450], [700, 450], [1170, dst.shape[0]] ], np.float32)
offset = 300
    dst_pts = np.array([ [0 + offset, dst.shape[0]], [0 + offset, 0], [dst.shape[1] - offset, 0], [dst.shape[1] - offset, dst.shape[0]] ], np.float32)
```

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 175, 720     | 300, 720        | 
| 590, 450      | 300, 0      |
| 700, 450     | 980, 0      |
| 1170, 720      | 980, 720        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![Warped Image Example][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

I identified pixels and fit them using a second order polynomial in `Final_Pipeline.ipynb` using the function `find_lane_lines_new_fit()`. Here is an example of an image with lane line pixels identified and a polynomial drawn through them.

![Polynomial Fit][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in the python notebook Lines_Class.ipynb in the function `get_curvature()`. I calculated the radius of curvature by first converting the left and right fit of x co-ordinates from pixels to meters. And also the y co-ordinates from pixels to meters. I then found a new fit using these transformed co-ordinates. Finally using the co-efficients of the new fit, I evaluated the radius of curvature of the lane, at the bottom of the image y = max(y coords). For calculating vehicle position I used the `get_vehicle_position` function. I calculated the difference between the center of the image, and center of the road (vehicle position assumed to be here). And then converted this to meters and depending on the sign of this value, reported the vehicle to be left or right of the center of the lane.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in `Lines_Class.ipynb` in the function `draw_poly()`.  Here is an example of my result on a test image:

![Final Output][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video_solution.mp4)


---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?
For the various parts of this project, I shall briefly outline the steps I took.
For thresholding, I took a combination of SobelX, SobelY, Magnitude Gradient and Direction thresholding for the gradients of the image.
And for color, I took HLS color space for yellow and HSV for white. There were some issues, in this as it is not so robust to shade and lighting, and may struggle in extreme conditions like snow.
To make it more robust, I could experiment with more colorspaces (maybe LAB)  and try out different combinations of these thresholds.
In addition to this I could try various combination of thresholding for gradient of the images.

I identified lane line pixels using a sliding window search method. And then fit a second order polynomial using these points for each lane. An improvement I could make to this method, is to play around with the margin, min_pixel and nWindows parameters to improve pixel finding accuracy. 

Using this fit, I calculated a set of fitted_x points for each lane (using the y co-ordinates ranging from 1 to the height of the image). Finally I plotted these fittedx points on the image. 

Finally, I created a `Line()` class to keep track of the properties (such as previous fittedx pixels, previous fit co-efficient etc.).
An improvement I can make using this information, could be to apply a criteria in my sanity check, that looks for large differences in these co-efficients over frames. If there is a large difference, then I dont update my lines with the information from this frame. I can also tweak the number of previous frames over which I average to get the best fitted_x pixels for both lanes.
