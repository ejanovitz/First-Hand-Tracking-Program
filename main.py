import cv2 as cv
import mediapipe as mp
import numpy
import pyautogui

# Capture video
webcam = cv.VideoCapture(0)

# cature our hands
my_hands = mp.solutions.hands.Hands()
# draw points on hand
drawing_utils = mp.solutions.drawing_utils

# Need to draw a line between Pointer and Thumb
x1 = y1 = x2 = y2 = 0

# Pointer finger purly
x3 = y3 = x4 = y4= 0

# Screen Width
screen_width, screen_height = pyautogui.size()

# Initialize mouse coordinates
mouse_x = mouse_y = 0

# Previous cursor position
prev_mouse_x = prev_mouse_y = 0

# Smoothing factor (adjust as needed)
smoothing_factor = 0.2

# Need to show captured image
while True:
    # Capture image from webcam
    # this function returns 2 variables and we don't need the first one
    # so lets just put an _ to discard it
    _, image = webcam.read()
    # 1 means flip x axis, y is 0
    image = cv.flip(image, 1)

    # Returns 3 variables
    frame_height, frame_width, _ = image.shape

    # Convert image from BGR to RGB
    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)

    # want to collect multiple hands
    hands = output.multi_hand_landmarks



    if hands:
        for x in hands:
            # drawing points
            drawing_utils.draw_landmarks(image, x)

            # Capture the finger points
            landmarks = x.landmark

            # collects all the points on the hands
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                # Pointer finger
                if id == 8:
                    # For the cursor
                    mouse_x = int(screen_width / frame_width * x)
                    mouse_y = int(screen_height / frame_height * y)

                    cv.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x1 = x
                    y1 = y

                # Base of pointer finger
                if id == 5:
                    cv.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x3 = x
                    y3 = y

                # Thumb
                if id == 4:
                    cv.circle(img=image, center=(x, y), radius=8, color=(255, 0, 0), thickness=3)
                    x2 = x
                    y2 = y

                # Middle fingertip
                if id == 12:
                    cv.circle(img=image, center=(x, y), radius=8, color=(255, 0, 255), thickness=3)
                    x4 = x
                    y4 = y


        # Volume control on/off
        volume_control_on = False

        pointer_distance = (y3 - y1) / 4
        #print("Pointer distance: ", pointer_distance)
        if pointer_distance < 5:
            volume_control_on = not volume_control_on

        dist = min(numpy.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / 4, 35)

        if not volume_control_on:
            if dist < 5:
                print("CLICK")
                pyautogui.click()

            distance_pointer_middle = int(min(numpy.sqrt((x4 - x1) ** 2 + (y4 - y1) ** 2) / 4, 35))

            print("Distance between pointer and middle: ", distance_pointer_middle)
            cv.line(image, (x1, y1), (x4, y4), (0, 255, 0), 5)

            # Interpolation
            smoothed_mouse_x = int((1 - smoothing_factor) * prev_mouse_x + smoothing_factor * mouse_x)
            smoothed_mouse_y = int((1 - smoothing_factor) * prev_mouse_y + smoothing_factor * mouse_y)

            if distance_pointer_middle < 5:
                print("MOVING CURSOR")
                # What actually moves the mouse
                pyautogui.moveTo(mouse_x, mouse_y)

        if volume_control_on:
            # will make the computer run faster since it's not constantly calculating
            # Drawing line
            # d = sqrt( (x_2 - x_1)^2 + (y_2 - y_1)^2 )
            # this will give a number between 0 - 100, but we want 0 - 35, so we are going to divide by 4

            # point 1, point 2, color, thickness
            cv.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)

            #print("Distance: ", dist)
            if dist > 17.5:
                # Increase volume
                pyautogui.press("volumeup")
            else:
                # Decrease volume
                pyautogui.press("volumedown")

    cv.imshow("Hand Volumn Control Using Python", image)

    key = cv.waitKey(10)

    # Esc key
    if key == 27:
        break;

webcam.release()
cv.destroyAllWindows()
