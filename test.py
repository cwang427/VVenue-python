import cognitive_face as CF
import sys
import time
from cv2 import *

"Authenticate API Key with Microsoft Cognitive Services Face API"
KEY = '26a1c49867934418bfcceac915443574'
CF.Key.set(KEY)

"Start UI Loop"
while True:
    print "Current Active Events: "
    for eve in CF.person_group.lists():
        print eve['personGroupId']
    print ""
    init_decision = True
    event, signUp, signIn  = False, False, False


    "Ask User for action"
    while init_decision:
        st = raw_input("What would you like to do?\n1. Create an event\n2. Sign up for an event\n3. Sign into an event\n")
        if st == "1" or st == "Create an event": event = True
        elif st == "2" or st == "Sign up": signUp = True
        elif st == "3" or st == "Sign in": signIn = True
        else: print "Invalid action"
        init_decision = False


    "Event Creation case"
    if event:
        made = False
        while not made:
            event_name = raw_input("What would you like to name your event?\n")
            event_ID = raw_input("What would you like your event ID to be? No upper-case letters, please.\n")
            try:
                CF.person_group.create(event_ID, event_name)
                made = True
                print "Your event, ", event_name, " has been created!\n"
            except:
                print "Event ID already taken! Please try again.\n"


    #"User Event Sign-Up case"
    elif signUp:


        "Sign-Up creation input data"
        event_ID = raw_input("What is the event ID of the event you are attending?\n")
        customer_name = raw_input("What would you like your login name to be?\n")
        user_data = raw_input("What would you like your keyword to be?\n")
        try:
            customer_ID = CF.person.create(event_ID, customer_name, user_data)
            print customer_ID
            print "Your personal ID is: ", customer_ID['personId'], "\nPlease remember it!\n"
            raw_input("After your next input, we will take your photo. This will occur three times for consistency.\n")
            photoCount = 0
            while photoCount < 3:

                "Open camera for photo use; close afterwards to prevent early picture taking"
                cam = VideoCapture(0)   # 0 -> index of camera
                s, img = cam.read()
                cam.release()
                if s:    # frame captured without any errors
                    namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
                    imshow("cam-test",img)
                    waitKey(4000)
                    destroyWindow("cam-test")

                satisfied = raw_input("Were you satisfied with that photo?\n")


                "Handles 3 photos for confidence and trains our person group"
                if satisfied == "yes" or satisfied == "Yes" or satisfied == "y" or satisfied == "Y":
                    imwrite("filename.jpg",img) #save image
                    try:
                        CF.person.add_face("filename.jpg", event_ID, customer_ID['personId'])
                        photoCount += 1
                        if photoCount <= 2:
                            raw_input("Your beautiful face has been recorded! Your next photo will be taken after your next input.\n")
                        elif photoCount == 3:
                            CF.person_group.train(event_ID)
                            print "Done! You will now return to the main screen.\n"
                    except:
                        raw_input("Face not detected in photo. Please try again after your next input.\n")
                else:
                    raw_input("Your photo will be retaken after your next input.\n")
        except:
            print "Event is not recognized!\n"


    #"User Event Sign-In case"
    elif signIn:
        eventFound = False
        event_ID = raw_input("What is the event ID you are attending?\n")
        while not eventFound:
            try:
                CF.person_group.get(event_ID)
                eventFound = True
            except:
                event_ID = raw_input("Event not found! What is the event ID you are attending?\n")

        raw_input("After your next input, your photo will be taken for verification.\n")
        verified = False
        if CF.person_group.get_status(event_ID)['status'] != "succeeded":
            verified = True
            print "Your event is currently processing faces. Please try again later.\n"
        while not verified:


            "Open camera for photo use; close afterwards to prevent early picture taking"
            cam = VideoCapture(0)   # 0 -> index of camera
            s, img = cam.read()
            cam.release()
            if s:    # frame captured without any errors
                namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
                imshow("cam-test",img)
                waitKey(4000)
                destroyWindow("cam-test")
            imwrite("filename.jpg",img)
            try:
                face = CF.face.detect('filename.jpg')
                faceID = face[0]['faceId']
                try:
                    try:
                        identify = CF.face.identify([faceID], event_ID)
                    except:
                        print "it actually failed"
                    print "Person identified as: ", CF.person.get(event_ID, identify[0]['candidates'][0]['personId'])['name']
                except:
                    print "identify failed"
                verified = True
            except:
                raw_input("Face not detected. Please try again.\n")