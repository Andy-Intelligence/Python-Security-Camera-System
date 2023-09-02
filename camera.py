import cv2 as cv
import threading
import imutils
import argparse
import numpy as np
import tensorflow as tf
import datetime
from process_cloud_storage import cloud_process


class Camera:

    capture = cv.VideoCapture(0)
    

    net = cv.dnn.readNetFromCaffe('C:\\Users\\user\\Desktop\\SecurityCamera\\MLmodels\\config.txt', "C:\\Users\\user\\Desktop\\SecurityCamera\\MLmodels\\mobilenet_iter_73000.caffemodel")
    out = None

    def __init__(self):
        # initialy the camera is not activated
        self.activate = False
        #this evaluates to false this thread is created once the camera wants to start running so that other processes don't affect it
        self.camera_operation_thread = None 

        # at this point i load the downloaded pretrained model using the tf.saved_model.load() method
        self.model = tf.saved_model.load(self.model_path)



    def start(self):
        if not self.activate and not self.camera_operation_thread: 
            self.camera_operation_thread = threading.Thread(target=self.run) 

        # this will start the camera thread
        self.camera_operation_thread.start()
        self.activate = True
        print(f'the camera has started')

        
    

    def stop(self):
        self.camera_operation_thread = None
        self.activate = False
        print(f'the camera hs stopped')
        return "the camera has stopped"
    

    




    def detect(self, frame):
        self.frame = frame
        #A blob is generated from the input frame using the cv.dnn.blobFromImage function. This is a preprocessing step 
        # that prepares the frame to be fed into a deep learning model.
        # The function takes the frame, a scale factor of 0.007843, target size of (300, 300),
        # and a mean subtraction of 127.5.
        blob = cv.dnn.blobFromImage(frame,0.007843,(300,300),127.5)
        #The blob is set as the input to a deep neural network (self.net) using the setInput 
        #function. Then, self.net.forward() 
        #performs the forward pass, generating detections.
        self.net.setInput(blob)
        detections = self.net.forward()
        person_detected = False


        #A loop iterates through the detections from the network. The confidence score and 
        #index (class ID) of the detection
        #are extracted from the detections array
        for i in range(detections.shape[2]):
            confidence = detections[0,0,i,2]


            idx = int(detections[0,0,i,1])

            #Inside the loop, the code checks if the class index (idx) is 15 
            #(which might correspond to a specific class, such as "person") and if the confidence is greater than 0.5. 
            #If these conditions are met, the code calculates the bounding box coordinates from the detection and scales them to 
            #match the frame dimensions. It then draws a green rectangle around the detected person using cv.rectangle.
            if idx == 15 and confidence > 0.5:
                box =  detections[0,0,i,3:7]*np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (startX, startY, endX, endY) = box.astype("int")
                cv.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                person_detected = True

        return person_detected


    def run(self):
        person_detected = False
        non_detected_counter = 0
        current_recording_name = None

        Camera.cap = cv.VideoCapture(0)

        while self.activate:
            success, frame = self.cap.read() #success returns boolean to decide if python is able to read videocapture frames
            # frame = cv.resize(frame,(640,640))
            # frame = cv.cvtColor(frame,cv.COLOR_RGB2GRAY)
            if not success:
                break
            else:
                
                # self.detect(frame)
                person_detected = self.detect(frame)

                if person_detected:
                    non_detected_counter = 0 #this will restart the couting of frames without a person but while a person is detected the count is kept at zero because someone is detected at every frame
                    if self.out is None:
                        now = datetime.datetime.now()
                        formatted_now = now.strftime("%d-%m-%y-%H-%M-%S")
                        print(f'person detected at {formatted_now}')
                        current_recording_name = f'{formatted_now}.mp4'
                        fourcc = cv.VideoWriter.fourcc(*'mp4v')
                        self.out = cv.VideoWriter(current_recording_name,fourcc,20.0,(frame.shape[1], frame.shape[0]))

                    self.out.write(frame)

                else:
                    #if someone is not detected the frame counter begins to count till 50 frames pass then it stops recording
                    non_detected_counter += 1 
                    if non_detected_counter >= 50:
                        if self.out is not None:
                            #stops recording
                            self.out.release() 
                            self.out = None
                            cloud_process.handle_detection(current_recording_name)
                            current_recording_name = None

            



            
                            

                cv.imshow("Security Camera", frame)

            if cv.waitKey(25) & 0xFF == ord('q'):
                break


        Camera.cap.release()
        cv.destroyAllWindows()
        print(f'the camera is running')
        return "the camera is running"


