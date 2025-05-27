from picamera2 import Picamera2
import cv2
import time
import numpy as np
from maestro import Controller
from cat_detect import get_cat_probability



# Initialize servo controller
servo = Controller()
servo.setSpeed(6, 5) # looking for a cat
servo.setSpeed(8, 10) # petting
servo.setSpeed(1, 5) # middle servo for the landing part
channel = 8  # Top servo channel number
change_amount = 50  #amount to change servo position of the petting motion

#####################################################################################
#SERVO LIMITS: STARTING AT 4000 and MAX is 8000
######################################################################################
def pet_loop():

    # setup both cameras
    picam1 = Picamera2(camera_num=1)
    preview_config = picam1.create_preview_configuration()
    picam1.configure(preview_config)
    picam1.start()

    picam2 = Picamera2(camera_num=0)
    preview_config = picam2.create_preview_configuration()
    picam2.configure(preview_config)
    picam2.start()
    
    

    #set initial position for all servos
    servo.setTarget(6, 4000)
    pos_6 = 4000
    
    servo.setTarget(1, 8000)
    pos_1 = 8000

    servo.setTarget(channel, 4000)
    current_pos = 4000

    #set booleans to for phases
    move_left = False
    cat_found = False
    petting = False

    while not cat_found:
        prob = get_cat_probability(picam1)
        print(f"Cat probability: {prob}")
        if prob >= 0.5: #probability threshold
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

    # LANDING
    dark_seq = 0

    try:
        while True:
            
            if not petting:
                #capture frame
                frame = picam2.capture_array()

                #convert to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY) # type: ignore

                print(np.median(gray))


                if np.median(gray) > 100:
                    print("ITS LIGHT")
                    time.sleep(0.5)
                    servo.setTarget(channel, current_pos + 80)
                    current_pos += 80
                    dark_seq = 0
                else:
                    print("ITS DARK")
                    time.sleep(0.5)
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
                #petting down
                for i in range(10):
                    servo.setTarget(channel, current_pos + change_amount)
                    current_pos += change_amount

                time.sleep(0.2)
                
                frame = picam2.capture_array()
                
                gray = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY) # type: ignore

                if np.mean(gray) > 110: #if the cat is gone means it is light again
                    picam1.close()
                    picam2.close()
                    return "gone"
                
                #petting up
                for i in range(10):
                    servo.setTarget(channel, current_pos - change_amount)
                    current_pos -= change_amount
                
                time.sleep(0.2)

                
        
    except KeyboardInterrupt:
        print("Stopping...")

    finally:
        servo.setTarget(channel, current_pos)
        picam1.stop()
        picam2.stop()
    return "Done"

#petting loop
while True:
    pet_loop()



