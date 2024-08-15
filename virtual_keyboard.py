import cv2
import mediapipe as mp
from time import time
from pynput.keyboard import Controller, Key
import threading

def start_virtual_keyboard():
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mpdraw = mp.solutions.drawing_utils

    keyboard = Controller()

    cap = cv2.VideoCapture(0)
    cap.set(2, 150)

    class Button():
        def __init__(self, pos, text, size=[70, 70]):
            self.pos = pos
            self.size = size
            self.text = text
            self.is_pressed = False

    keys = [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
        ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "\\"],
        ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "ENTER"],
        ["BKSP", "WINDOWS", "VOL UP", "VOL DOWN", "CAPS", "SCREEN UP", "SCREEN DOWN", "QUIT"]
    ]

    def drawAll(img, buttonList):
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            if button.is_pressed:
                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
            else:
                cv2.rectangle(img, button.pos, (x + w, y + h), (96, 96, 96), cv2.FILLED)
            cv2.putText(img, button.text, (x + 10, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        return img

    buttonList = []

    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([70 * j + 10, 70 * i + 10], key, size=[60, 60]))

    app = 0
    last_key_time = time()

    while True:
        success, frame = cap.read()
        frame = cv2.resize(frame, (1000, 580))
        frame = cv2.flip(frame, 1)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img)
        landmark = []

        frame = drawAll(frame, buttonList)

        if results.multi_hand_landmarks:
            for hn in results.multi_hand_landmarks:
                for id, lm in enumerate(hn.landmark):
                    hl, wl, cl = frame.shape
                    cx, cy = int(lm.x * wl), int(lm.y * hl)
                    landmark.append([id, cx, cy])

            if len(landmark) >= 2:
                x1, y1 = landmark[8][1], landmark[8][2]
                x2, y2 = landmark[12][1], landmark[12][2]

                distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

                if distance < 50:
                    for button in buttonList:
                        xb, yb = button.pos
                        wb, hb = button.size

                        if (xb < x1 < xb + wb) and (yb < y1 < yb + hb):
                            k = button.text

                            current_time = time()
                            if current_time - last_key_time > 0.5:
                                if k == "ENTER":
                                    keyboard.press(Key.enter)
                                    keyboard.release(Key.enter)
                                elif k == "BKSP":
                                    keyboard.press(Key.backspace)
                                    keyboard.release(Key.backspace)
                                elif k == "WINDOWS":
                                    keyboard.press(Key.cmd)
                                    keyboard.release(Key.cmd)
                                elif k == "VOL UP":
                                    keyboard.press(Key.media_volume_up)
                                    keyboard.release(Key.media_volume_up)
                                elif k == "VOL DOWN":
                                    keyboard.press(Key.media_volume_down)
                                    keyboard.release(Key.media_volume_down)
                                elif k == "CAPS":
                                    keyboard.press(Key.caps_lock)
                                    keyboard.release(Key.caps_lock)
                                elif k == "SCREEN UP":
                                    keyboard.press(Key.brightness_up)
                                    keyboard.release(Key.brightness_up)
                                elif k == "SCREEN DOWN":
                                    keyboard.press(Key.brightness_down)
                                    keyboard.release(Key.brightness_down)
                                elif k == "QUIT":
                                    keyboard.press(Key.alt_l)
                                    keyboard.press(Key.f4)
                                    keyboard.release(Key.f4)
                                    keyboard.release(Key.alt_l)
                                else:
                                    keyboard.press(k)
                                    keyboard.release(k)

                                button.is_pressed = True
                                last_key_time = current_time
                            break
                else:
                    for button in buttonList:
                        button.is_pressed = False

        cv2.imshow('virtual keyboard', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def stop_virtual_keyboard():
    cv2.destroyAllWindows()
