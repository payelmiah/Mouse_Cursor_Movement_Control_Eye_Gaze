import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
on=False

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            #cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)
                cv2.putText(frame, "system: "+("on" if on else "off"), (0, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 25, 0), 2,
                            cv2.LINE_AA)
                cv2.putText(frame, ("x: "+str(round(screen_x,2))), (0, 135), cv2.FONT_HERSHEY_COMPLEX, .5, (255, 255, 255), 1,
                            cv2.LINE_AA)
                cv2.putText(frame, ("x: "+str(round(screen_x,2))), (0, 135), cv2.FONT_HERSHEY_COMPLEX, .5, (0, 0, 0), 1, cv2.LINE_AA)

                cv2.putText(frame, ("Y: "+str(round(screen_y,2))), (0, 155), cv2.FONT_HERSHEY_COMPLEX, .5, (255, 255, 255), 1,
                            cv2.LINE_AA)
                cv2.putText(frame, ("Y: "+str(round(screen_y,2))), (0, 155), cv2.FONT_HERSHEY_COMPLEX, .5, (0, 0, 0), 1, cv2.LINE_AA)

        #for left eye
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        #print(left[0].y-left[1].y)

        if ((left[0].y - left[1].y) < 0.004) and on:
            print('click')
            cv2.putText(frame, "left click", (0, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (220, 20, 60), 4, cv2.LINE_AA)
            cv2.putText(frame, "left click", (0, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (220, 20, 60), 2, cv2.LINE_AA)
            pyautogui.click()
            pyautogui.sleep(1)

            pyautogui.click()
            pyautogui.sleep(1)

        #for right eye
        right = [landmarks[374], landmarks[386]]
        for landmark in right:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        #print(right[0].y-right[1].y)
        cv2.putText(frame, "EAR: "+str(round(((right[0].y-right[1].y)+(left[0].y-left[1].y))*7.66,2)), (0, 350), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(frame, "EAR: "+str(round(((right[0].y-right[1].y)+(left[0].y-left[1].y))*7.66,2)), (0, 350), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)

        if ((right[0].y - right[1].y) < 0.004) and on:
            print('click')
            cv2.putText(frame, "right click", (0, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 4, cv2.LINE_AA)
            cv2.putText(frame, "right click", (0, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            pyautogui.click(button='right')
            pyautogui.sleep(1)

            pyautogui.click()
            pyautogui.sleep(1)

        #Mouth for activate/deactivate mouse
        mouth = [landmarks[14], landmarks[13]]
        for landmark in mouth:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        print(mouth[0].y-mouth[1].y)
        #cv2.putText(frame, "EAR: "+str(((mouth[0].y-mouth[1].y)+(left[0].y-left[1].y))*7.66), (0, 350), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3, cv2.LINE_AA)
        #cv2.putText(frame, "EAR: "+str(((mouth[0].y-mouth[1].y)+(left[0].y-left[1].y))*7.66), (0, 350), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)

        if (mouth[0].y - mouth[1].y) > 0.06:
            #print('click')
            #cv2.putText(frame, "right click", (0, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 4, cv2.LINE_AA)
            #cv2.putText(frame, "right click", (0, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            #pyautogui.click(button='right')
            #pyautogui.sleep(1)
            if not on:
                on=True
            else:
                on=False
            #pyautogui.click()
            #pyautogui.sleep(1)
        #rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        font = cv2.FONT_HERSHEY_SIMPLEX

        if results.multi_hand_landmarks:
            for handLMS in results.multi_hand_landmarks:
                # https://google.github.io/mediapipe/solutions/hands.html
                # mpDraw.draw_landmarks(rgb_frame, handLMS, mpHands.HAND_CONNECTIONS)
                lmList = []
                for id, lm in enumerate(handLMS.landmark):
                    h, w, c = rgb_frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                    # use landmark map to identify the point you want to highlight
                    # if id == 12:
                    # cv2.circle(rgb_frame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                on=True
                indexX = 0
                indexY = 0
                indexMid = 0
                handBottomX = 0
                handBottomY = 0
                pinkyX = 0
                pinkyY = 0
                fistWarning = "Fist!"
                for lms in lmList:
                    if lms[0] == 7:
                        indexX, indexY = lms[1], lms[2]
                        # cv2.circle(rgb_frame, (lms[1], lms[2]), 15, (255, 0, 255), cv2.FILLED)
                    elif lms[0] == 5:
                        indexMid = lms[2]
                    # elif lms[0] == 11:
                    # middleY = lms[2]
                    # cv2.circle(rgb_frame, (lms[1], lms[2]), 15, (255, 0, 255), cv2.FILLED)
                    # elif lms[0] == 15:
                    # ringY = lms[2]
                    # cv2.circle(rgb_frame, (lms[1], lms[2]), 15, (255, 0, 255), cv2.FILLED)
                    elif lms[0] == 19:
                        pinkyX, pinkyY = lms[1], lms[2]
                        # cv2.circle(rgb_frame, (lms[1], lms[2]), 15, (255, 0, 255), cv2.FILLED)
                    elif lms[0] == 0:
                        handBottomX, handBottomY = lms[1], lms[2]
                if (indexY < handBottomY) and (indexY > indexMid):
                    cv2.rectangle(rgb_frame, (indexX, indexY), (pinkyX, handBottomY), (0, 0, 255), 2)
                    cv2.putText(rgb_frame, fistWarning, (pinkyX + 2, indexY - 2), (font), .7,
                                (0, 0, 255), 1, cv2.LINE_4)
                    print("Fist!!")
                    on = False

    cv2.imshow('Gaze Controlled Mouse', frame)
    cv2.waitKey(1)