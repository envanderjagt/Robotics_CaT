from picamera2 import Picamera2
import cv2
import time
import numpy as np
from maestro import Controller
from cat_detect import get_cat_probability






# # get the mean value wihtout any detection
# frame = picam2.capture_array()

# # Convert to grayscale
# gray = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY) # type: ignore

# baseline_mean = np.mean(gray)

# Initialize servo controller
servo = Controller()
servo.setSpeed(6, 5)
servo.setSpeed(8, 10) # petting
servo.setSpeed(1, 5)
channel = 8  # Servo channel number
change_amount = 50  # Amount to change servo position

#####################################################################################
#STARTING AT 4000 adn MAX is 8000
######################################################################################
def pet_loop():
    picam1 = Picamera2(camera_num=1)
    preview_config = picam1.create_preview_configuration()
    picam1.configure(preview_config)
    picam1.start()


    picam2 = Picamera2(camera_num=0)
    preview_config = picam2.create_preview_configuration()
    picam2.configure(preview_config)
    picam2.start()
    
    petting = False
    servo.setTarget(6, 4000)  # Set initial position for other servos
    pos_6 = 4000


    servo.setTarget(1, 8000)
    pos_1 = 8000


    servo.setTarget(channel, 4000)
    current_pos = 4000

    move_left = False
    cat_found = False


    while not cat_found:
        prob = get_cat_probability(picam1)
        print(f"Cat probability: {prob}")
        if prob >= 0.5:
            print("Cat detected! STOPPING!")
            time.sleep(1)
            cat_found = True
        else:
            if pos_6 == 4000:
                move_left = False
            elif pos_6 == 8000:
                move_left = True
            if move_left:
                servo.setTarget(6, pos_6 - 200)
                pos_6 -= 200
            else:
                servo.setTarget(6, pos_6 + 200)
                pos_6 += 200

            
        print(pos_6)


    print("DONE LOOKING< I FOUND A CAT")


    dark_seq = 0

    # TODO: ADD A CLAUSE THAT MAKES THE WHILE LOOP START AGAIN FROM THE START IF LIGHT VALUES HAVE BEEN DETECTED FOR MORE THAN 5 TIMES
    # TODO: FIND A SCRATCHER FOR AT THE EDGE
    # TODO: REINFORCE THE BASE WITH SCREWS 
    # TODO: FIX THE CHOPSTICK SO THAT IT IS MORE STURDY
    # TODO: PLUSHIE?
    try:
        while True:
            
            if not petting:
                # Capture frame
                frame = picam2.capture_array()

                # Convert to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY) # type: ignore

                print(np.median(gray))


                if np.median(gray) > 100:
                    print("ITS LIGHT")
                    #servo.setTarget(1, pos_1 - 40)
                    time.sleep(0.5)
                    servo.setTarget(channel, current_pos + 80)
                    current_pos += 80
                    #pos_1 -= 40
                    dark_seq = 0
                else:
                    print("ITS DARK")
                    #servo.setTarget(1, pos_1 + 40)
                    time.sleep(0.5)
                    #servo.setTarget(channel, current_pos + 80)
                    #current_pos += 80
                    #pos_1 += 40
                    dark_seq += 1
                time.sleep(0.5)

                if dark_seq > 2:
                    petting = True

                if current_pos >= 8000:
                    picam1.close()
                    picam2.close()
                    return "CAT gone..."


            else:
                print("PETTING!")
                for i in range(10):
                    servo.setTarget(channel, current_pos + change_amount)
                    current_pos += change_amount

                time.sleep(0.2)
                
                frame = picam2.capture_array()

                # Convert to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY) # type: ignore

                if np.mean(gray) > 110:
                    picam1.close()
                    picam2.close()
                    return "gone"
                
                
                for i in range(10):
                    servo.setTarget(channel, current_pos - change_amount)
                    current_pos -= change_amount
                
                time.sleep(0.2)

                
        
        # print(f"Left: {left_avg:.1f}, Right: {right_avg:.1f}")

        # # Threshold difference to avoid jitter
        # threshold = 10
        # current_pos = servo.getPosition(channel)

        # if left_avg + threshold < right_avg:
        #     print("Dark on left → moving servo left")
        #     servo.setTarget(channel, current_pos + change_amount)
        # elif right_avg + threshold < left_avg:
        #     print("Dark on right → moving servo right")
        #     servo.setTarget(channel, current_pos - change_amount)
        # else:
        #     print("Even lighting → centering servo")
        #     servo.setTarget(channel, current_pos)

        # # time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopping...")

    finally:
        servo.setTarget(channel, current_pos)
        picam1.stop()
        picam2.stop()
    return "WTF"

while True:
    pet_loop()



