"""
Main
Bỏi: NKDuy
"""

import cv2
import nkdcv  # pip install nkdcv-python
from nkdcv.HandTrackingModule import HandDetector
# pip install mediapipe==0.8.7
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
colorR = (255, 0, 255)

cx, cy, w, h = 100, 100, 200, 200


class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # Nếu đầu ngón tay trỏ nằm trong vùng hình tứ giác
        if (cx - w // 2) < cursor[0] < (cx + w // 2) and (cy - h // 2) < cursor[1] < (cy + h // 2):
            self.posCenter = cursor


rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 150]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList:
        l, _, _ = detector.findDistance(8, 12, img, draw=False)
        print(l)
        if l < 40:
            cursor = lmList[8]  # dấu vân tay

            # gọi hàm update() ở đây
            for rect in rectList:
                rect.update(cursor)

    # Bản vẽ rõ
    # for rect in rectList:
    #     cx, cy = rect.posCenter
    #     w, h = rect.size
    #     cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
    #     nkdcv.cornerRect(img, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    # Bản vẽ trong suốt
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        nkdcv.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Virtual Drag Drop", out)
    cv2.waitKey(1)
