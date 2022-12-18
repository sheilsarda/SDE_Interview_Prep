# Python Solution Docs

- To run program: (i) make sure `python3` is installed; (ii) navigate to the directory containing `main.py`; (iii) execute `python3 main.py`
- Door starts off in the closed state and by default takes 5 seconds (wall time) to open / close. These times are customizable parameters in the `__init__` method
- Safety function can be triggered by typing `safety` in the command line as the door is closing (i.e., `door.__current_state == Start_Closing`)

# Remedy Robotics Technical Screen

We designed these questions to help us understand your proficiency with programming as well as your problem solving abilities.

As you are completing the questions, please set up a local github repo (not published on the internet) for the coding interview and commit as you complete each question. This way we have an approximate sense of how long each question took you by looking at the git log. 

*IMPORTANT* The objective is to demonstrate your abilities! Please try and avoid getting bogged you down with minutiae. Your time is valuable!

Once complete, please email back your answers in a zip file.

# Garage Door

We’re building a robot capable of doing autonomous brain surgery.
However, due to time constraints, we'll be solving a much less ambitious
problem. You will be designing a garage door controller.

Your garage door controller should meet the following specs:

1.  An input from the user (keyboard stroke is fine) moves the door toward the opposite state

    Ex: `open, trigger, starts closing, closed.` `closed, trigger, starts opening, open`
1.  If the user hits the input while it’s in motion, the door should enter the freeze state. The next time the input is triggered after the freeze, it should send the door in the opposite direction.

    Ex: `open, trigger, starts closing, trigger, freezes, trigger, starts opening, open`.
1.  There’s a safety sensor that triggers when something passes in the path of the door when it’s closing. In response to the safety trigger, the door should stop closing and start opening.

    Ex: `open, trigger, starts closing, safety trigger, starts opening, open`.
1. Write at least one unit test to verify the performance

## Your Task

Your tasks are to

a. Draw a State Diagram of the system

b. Code the solution in Python, constructing at least one class and
providing a simple readme. We will run the code and initiate the user input and
the safety trigger to test it.

c. Convert your Python code to C++. Again, construct at least one class and
provide a simple readme. We will run the code and initiate the user input and
the safety trigger to test it.

## Time estimate

Around 2 hours
