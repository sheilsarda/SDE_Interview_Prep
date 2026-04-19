# Autonomous Systems Interview Preparations

> This document contains some interview questions as provided in Udacity's Robotics Engineer Nanodegree program.

## Project Instructions

### Role Selection

It's time for you to practice your interviewing skills! Over the next several pages, you'll see that we have specific roles in Autonomous Systems,
just like the videos you watched before:

- Perceptions/Sensors
- Deep Learning
- Motion Planning
- Mapping/Localization
- Control

First, you need to select a single role that you are interested in. While you are welcome to read through and practice any of the questions under the other pages,
for the project, you are going to focus on just one area. We've also included a General page that has some additional questions you can practice, but aren't part of the project itself.

### Question Selection for Your Role
Once you've decided on a role, you can click on that role's page for a list of related questions. While we'll repeat these requirements again for simplicity
on each page, for your selected role, you'll need to:

- Answer the **required** question related to a recent project you've worked on, similar to the My Own Project video you watched earlier
- Select and answer **three** questions specifically related to your role from the page
- At least one of the three role-specific questions **must be** a coding-based question marked with **[Code]**.
- You are welcome to include code or any desired drawings and diagrams to further detail your answers for other questions as well, although it is not required.
  We do encourage you to do this for all your answers though, as that would likely be what your interviewer desires from you!

### Question Follow-ups
You may have noticed throughout the interview videos before that the interviewers have follow-up questions to extend their original questions,
or to clarify something the candidate discussed. In order to pass the project, you should also clearly denote at least one potential relevant
follow-up question for each question above, and also provide a sufficient answer for it.

---

## Perception/Sensor Engineer

So, you're interested in a role as a Perception/Sensor Engineer? Great choice! Below, you will find one general question, as well as a list of Perception/Sensor Engineer-specific questions. To complete the project, you'll need to complete the general question along with three questions from the role-specific list, with at least one of them needing to be marked as requiring code with [Code]. While it isn't required to use code in the other two, we highly encourage you to either code, diagram or draw any relevant information for your answers in the other questions as well.

Make sure not to just select questions in areas you are most comfortable with! You likely won't get so lucky in a real interview situation.

### Required question

Explain a recent project you've worked on. Why did you choose this project? What difficulties did you run into this project that you did not expect, and how did you solve them?

### Perception/Sensor Engineer questions

_Pick three of these questions, including at least one marked [Code]._

- Explain your lane detection algorithm. How can it be improved? How does it account for curves and hills? How could you integrate machine learning techniques into the algorithm?
- What are some of the advantages & disadvantages of cameras, lidar and radar? What combination of these (and other sensors) would you use to ensure appropriate and accurate perception of the environment?
- How do features from algorithms like SIFT, SURF and HOG differ? Explain how these algorithms work, and how you would use them within a perception pipeline.
- Explain the technique behind Hough Transforms. Where would this type of feature extraction be useful?
- **[Code]** What is the RANSAC algorithm? Code the steps that this algorithm takes to help deal with outliers in data. How can we use this algorithm for computer vision?
- Describe the overall process of how a basic Kalman Filter works. Where might a basic Kalman Filter be less than sufficient? How can you improve the basic algorithm to improve performance in such a situation?
- How does an Extended Kalman Filter differ from a regular Kalman Filter? Provide an example of where an EKF would be necessary or an improvement, and detail why it would be needed in that situation.
- What is the difference between an Extended Kalman Filter and an Unscented Kalman Filter? In what situations would there be larger differences between the two approaches?
- **[Code]** Explain the steps behind how an Extended Kalman Filter is implemented.
- Have you worked with point clouds and/or the Point Cloud Library (PCL) before? If you’ve used PCL before, which modules of PCL did you use, and what application did you use it toward?
- **[Code]** Describe how a particle filter works, where it is useful, and how it performs against similar algorithms. Code an example of how you update the weights of the particles between steps.
- Your perception subsystem has noticed an object in the path of your robot, but it has failed to determine what the object is. How would your perception subsystem further handle this situation?
- **[Code]** What approach would you take if the various sensors you are using have different refresh rates?
- **[Code]** 3D point clouds are sometimes processed into "voxels" as one step into object detection. 1) What is a voxel, 2) What is the process behind converting point cloud data into voxels (code this), and 3) Why would we want to perform this step with our point cloud data?

---

## Deep Learning Engineer

So, you're interested in a role as a Deep Learning Engineer? Great choice! Below, you will find one general question, as well as a list of Perception/Sensor Engineer-specific questions. To complete the project, you'll need to complete the general question along with three questions from the role-specific list, with at least one of them needing to be marked as requiring code with [Code]. While it isn't required to use code in the other two, we highly encourage you to either code, diagram or draw any relevant information for your answers in the other questions as well.

Make sure not to just select questions in areas you are most comfortable with! You likely won't get so lucky in a real interview situation.

### Required question

Explain a recent project you've worked on. Why did you choose this project? What difficulties did you run into this project that you did not expect, and how did you solve them?

###  Learning Engineer questions

_Pick three of these questions, including at least one marked [Code]._

- Given different train/test accuracy curves, describe what is going on and how to address it (overfitting, learning rate too high, etc.)
- What is the difference between object classification and detection? How do any related architectures often differ to accomplish these tasks?
- How do you deal with severely unbalanced data? In what situations might this occur?
- How do you reduce overfitting in a neural network? What is regularization, and how does it impact overfitting?
- Say you have collected camera data from a mobile robot in which you would like to denote various objects of multiple classes with bounding boxes. How would you go about annotating these objects in your dataset? How would your answer change if instead of bounding boxes, you used semantic segmentation? What about instance segmentation?
- Say you have collected 3D data from a mobile robot in which you would like to denote various objects of multiple classes with bounding boxes. How would you go about annotating these objects in your dataset?
- Given a dataset of images or 3D data over time, what do you need to consider in creating training and validation data? How would you create your test set to test a related trained network?
- Explain the concepts behind Deep Reinforcement Learning, and how you would implement such a technique toward Motion Planning. How would you determine the reward functions to use? Would your implementation generalize well towards new, previously unseen environments?
- Have you deployed any models you have trained and tested into any production systems, or otherwise used on hardware outside of the same computer you trained the network on, such as an embedded system? What additional steps did you take to implement the model, and what type of testing did you perform to ensure appropriate performance?
- **[Code]** Explain a recent deep learning research paper you read and how it improved upon existing methods. What were its strengths and weaknesses? Code a mock-up of the network used in this paper in your desired deep learning library.
- **[Code]** Explain the ResNet neural network architecture. What were some of the key insights of this architecture compared to previous approaches, and why do they result in improvements in performance? Code an example of how to use residual layers in your desired deep learning library.
- **[Code]** Explain the GoogLeNet/Inception neural network architecture. What were some of the key insights of this architecture compared to previous approaches, and why do they result in improvements in performance? Code an example of how to use inception layers in your desired deep learning library.
- **[Code]** Explain the MobileNet neural network architecture. What were some of the key insights of this architecture compared to previous approaches, and why do they result in improvements in speed performance? Code an example of how to implement MobileNet in your desired deep learning library, and compare it to layers in other neural networks, noting why inference speed is improved.
- Describe behavioral cloning. How would you go about gathering quality data for this?
- What is dropout, and what is it used for? Let’s say we have a dropout layer with 50% drop probability. How would you scale the inputs/outputs between train and inference time? What if the drop probability is 75%?
- Explain why a convolutional neural network typically performs better on image-related tasks that a fully-connected network.
- **[Code]** Why do vanilla convolutional neural networks (just convolutions followed by pooling layers, out into fully-connected layers) often struggle in determining where in an image an object resides, and how have more recent methods improved in this area?
- Explain how backpropagation works.
- **[Code]** Given a dataset of your choosing, code a neural network in a deep learning library of your choice to train a model to do some type of inference over the data. Include any pre-processing steps. Explain why you chose the type of inference you did, as well as what you could apply your trained model to do.

---

## Motion Planning Engineer

So, you're interested in a role as a Motion Planning Engineer? Great choice! Below, you will find one general question, as well as a list of Perception/Sensor Engineer-specific questions. To complete the project, you'll need to complete the general question along with three questions from the role-specific list, with at least one of them needing to be marked as requiring code with [Code]. While it isn't required to use code in the other two, we highly encourage you to either code, diagram or draw any relevant information for your answers in the other questions as well.

Make sure not to just select questions in areas you are most comfortable with! You likely won't get so lucky in a real interview situation.

### Required question

Explain a recent project you've worked on. Why did you choose this project? What difficulties did you run into this project that you did not expect, and how did you solve them?

### Deep Learning Engineer questions

_Pick three of these questions, including at least one marked [Code]._

- **[Code]** 1) Explain the A* search algorithm. 2) What is one way to improve upon this algorithm for usage in real-world scenarios?
- You have a robot on a map with some obstacles on the map. The goal is in the corner of the map. How do you navigate the robot from its current position to the goal?
- Explain some of the different techniques used for global planning (such as at a city map level) vs. micro planning (such as planning on how to go from the entrance of a parking lot to a desired space). Show how you could implement techniques from these levels into one end-to-end algorithm to guide a mobile robot from one distant location to another.
- Explain the concepts behind Deep Reinforcement Learning, and how you would implement such a technique toward Motion Planning. How would you determine the reward functions to use? Would your implementation generalize well towards new, previously unseen environments?
- How do you would generate a desired trajectory over a fixed time horizon for a robot traveling at high speed? Consider what information you would need in order to determine a reasonable trajectory, as well as any additional constraints you may need to consider.
- **[Code]** Assume you have data of various robot trajectories around your own, in which you would like to build a model to predict the other robots’ behaviors, making sure that your own expensive robot is not damaged by collisions. Your robot does not have the benefit of GPU acceleration. Choose a classification technique in order to learn to predict behaviors, and explain your choice. Then, code an example of how you would build, train and implement this model.
- What is the difference between a data-based approach versus a model-based approach for behavior prediction? Explain the advantages and disadvantages of each, as well as you could implement the separate techniques.
- How can Partially observable Markov decision processes (POMDPs) be utilized in Motion Planning? How does the number of belief states in POMDPs relate to the state space of your robot, and how can that impact the performance or usability of this method in real-world applications?
- **[Code]** Explain the concepts behind a rapidly-exploring random tree (RRT), and implement an example in code.
- Explain how lattice planning can be used to discretize and simplify the paths through search space. Construct an example of a simple search space to show how this method works.
- Given a vehicle driving on a highway with other cars around it as well as potential stop lights and pedestrian crossings, and assuming perfect information from sensor data, construct a behavior tree/finite state machine for the vehicle's motion.
- **[Code]** 1) Explain the D* search algorithm (also known as Dynamic A*). 2) What is one way to improve upon this algorithm for usage in real-world scenarios?

---

## Mapping/Localization Engineer

So, you're interested in a role as a Mapping/Localization Engineer? Great choice! Below, you will find one general question, as well as a list of Perception/Sensor Engineer-specific questions. To complete the project, you'll need to complete the general question along with three questions from the role-specific list, with at least one of them needing to be marked as requiring code with [Code]. While it isn't required to use code in the other two, we highly encourage you to either code, diagram or draw any relevant information for your answers in the other questions as well.

Make sure not to just select questions in areas you are most comfortable with! You likely won't get so lucky in a real interview situation.

### Required question

Explain a recent project you've worked on. Why did you choose this project? What difficulties did you run into this project that you did not expect, and how did you solve them?

### Mapping/Localization Engineer questions

_Pick three of these questions, including at least one marked [Code]._

- How does Simultaneous Localization and Mapping (SLAM) differ from other localization approaches? What are the benefits and detriments of this over other approaches?
- **[Code]** Describe how a particle filter works, where it is useful, and how it performs against similar algorithms. Code an example of how you update the weights of the particles between steps.
- Describe the differences between dense mapping vs. sparse mapping. In what situations would you prefer the use of one over the other?
- **[Code]** Sparse mapping involves the use of “landmarks” in your map to assist with determining where your robot is in the environment. Given a set of detections and a map of landmarks (you may create a test set of these, which should not exactly match up), code a method to estimate where your robot is.
- Image-based localization concerns utilizing only camera images in order to determine location in an environment. Explain a method to implement such a system, as well as what the strengths and weaknesses of such an approach are.
- **[Code]** Why would you utilize an inertial measurement unit (IMU) in conjunction with GPS in localizing a moving robot? Implement a basic system that uses these together for accurate localization.
- **[Code]** How does GNSS+RTK (real-time kinematic) allow for higher accuracy than standard GPS systems? Implement a basic system that shows how this technique works.
- **[Code]** You have a robot in an environment with certain known landmarks, but its current position is unknown. Code a method to detect its new location over time when the robot has perfect movement and noisy sensor data. What would you need to change in this function if the robot's motion is also noisy?

---

## Control Engineer

So, you're interested in a role as a Control Engineer? Great choice! Below, you will find one general question, as well as a list of Perception/Sensor Engineer-specific questions. To complete the project, you'll need to complete the general question along with three questions from the role-specific list, with at least one of them needing to be marked as requiring code with [Code]. While it isn't required to use code in the other two, we highly encourage you to either code, diagram or draw any relevant information for your answers in the other questions as well.

Make sure not to just select questions in areas you are most comfortable with! You likely won't get so lucky in a real interview situation.

### Required question

Explain a recent project you've worked on. Why did you choose this project? What difficulties did you run into this project that you did not expect, and how did you solve them?

### Control Engineer questions

_Pick three of these questions, including at least one marked [Code]._

- What are some of the typical variables of motion that kinematic models often simplify or ignore in their calculations? In what situations might these models therefore fail, and how can you improve upon these types of models?
- An important consideration in control is the latency in between the calculation of a control movement and the actuation of said control movement. Given a 100ms delay, how would you account for this your controller?
- What is the bicycle model in kinematics? Make a diagram of it. How does this compare to the movement of a four-wheeled vehicle like a car, and why is it often sufficient in many cases to approximate the movement of a more complex vehicle?
- Describe how you could implement the Ackerman steering model for a four-wheeled robot, including describing the model itself. How does this compare to a steering model in which two of the wheels are turned at the same angle with respect to an axle? Is this model an approximation of ideal steering conditions?
- What is the differential drive model, and why is it particularly popular for robotics applications? How does this differ from a modern car?
- What are the primary differences between kinematic and dynamic models of control? In what situations are these types of models most similar, and when do they diverge? Include in your answer any necessary diagrams that may help to illustrate your point.
- Hans B. Pacejka produced tire models colloquially referred to as the “magic formula” for tire models. Explain the basis of his models, as well as how you would implement one of these in a robotics system. What forces must be considered in utilizing one of his tire models?
- Explain the concepts of slip angles and slip ratios with regards to tires. How would you account for these within a control model? In what situations would accounting for these be unimportant?
- **[Code]** How does a linear-quadratic regulator (LQR) differ from PID control? Does it require a given time horizon, and does it require continuous or discrete timesteps? Code an instance of a LQR given your own selection of time horizon and discrete/continuous, assuming you otherwise already have any necessary inputs.
- Suppose you built a line following robot. You created a line on the ground, put the robot on the line, but the robot oscillates back and forth rapidly once it is on the line. How would you fix this?
- Explain how model predictive control can be used to optimize control actuations over a given time horizon. What additional information can MPC take into account that PID control typically does not? How do you determine the constraints involved with MPC?
- **[Code]** In PID Control, if a robot is in between two waypoints of a desired trajectory, how is the cross track error determined? Code a method to calculate this. What information does this require from any other subsystems outside of the control system, and how would you account for any potential noise in that data (or alternatively, do you need to)?

---

## Other General Questions

While the below questions are not included under the specific roles for the project, you might consider doing some additional research or thinking about these areas depending on the role or company you are interviewing for.

These are not eligible to be used as a question and answer to be included in your project, but might give you some ideas of areas to talk about in your interview if you have experience with them.

### General Questions

- What is the importance of simulation in the testing of autonomous systems? What additional items do you need to consider in order to leverage this type of testing (or training) to real-world environments?
- How would you ensure all necessary information is logged for debugging purposes of your autonomous system?
- What tests or architectures do you need to implement to ensure that the integration of a module you have added to a system cannot cause a complete failure of the system if it alone fails?
- What is the difference between an embedded system and a real-time system?
- What is a real-time operating system and how does it differ from an operating system like Windows? Why are they often necessary for use in robotics applications, such as self-driving cars?
- What experience do you have with any open source self-driving car platforms, such as Autoware or Apollo? If you’ve helped contribute, explain what you contributed and how you appropriately documented any pull requests or commits. If you’ve utilized them as part of a project, explain how you integrated these platforms with your work.
- What experience do you have with any open source robotics platforms, such as ROS or Gazebo? If you’ve helped contribute, explain what you contributed and how you appropriately documented any pull requests or commits. If you’ve utilized them as part of a project, explain how you integrated these platforms with your work.
- What are the Society of Automotive Engineers (SAE) levels of automation? Pick three vehicles available commercially or in testing and place at least one of their systems into a level, and explain why it falls into that level.
