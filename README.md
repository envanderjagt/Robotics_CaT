# Robotics_CaT read me

# Assembly
Attach the two cameras tot he raspberrypi, then connect the pi to the maestro. Make sure the top servo is inserted into maestro channel 8, the middle servo into channel 1, and the bottom servo into channel 6. Then, add  the battrey power supply to the maestro as well and plug in the raspberry pi.

# Running the code
Make sure you have the same packages installed by running:
pip install -r requirementsCaT.txt
Then you can run the code by running:
python petting.py

# Calibration
Make sure that you calibrate the darkness value to a suitable value, since the lighting of every room is different. You can do this by measuring the darkness values seen when putting the fibers into some fur and what the values are when they are not inside of something but in the open. Usually, a value of around 105 suffices.
