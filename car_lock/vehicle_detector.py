#车辆检测
import cv2
import numpy as np
from config import MIN_VEHICLE_AREA, DILATE_ITERATIONS, ERODE_ITERATIONS


class VehicleDetector:
    def __init__(self):
        # 初始化背景减法器（MOG2算法，适用于动态背景）
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=16, detectShadows=True
        )

    def detect_vehicles(self, frame):
        """
        输入：原始帧
        输出：车辆轮廓列表、前景掩码（用于可视化）
        """
        # 1. 转换为灰度图（减少计算量）
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 2. 背景减法（提取前景：车辆+阴影）
        fg_mask = self.bg_subtractor.apply(gray)

        # 3. 阈值处理（去除阴影，只保留车辆前景）
        _, thresh = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)

        # 4. 形态学操作（膨胀+腐蚀，强化轮廓、去除噪点）
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilated = cv2.dilate(thresh, kernel, iterations=DILATE_ITERATIONS)
        eroded = cv2.erode(dilated, kernel, iterations=ERODE_ITERATIONS)

        # 5. 查找车辆轮廓
        contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 6. 过滤小轮廓（排除非车辆噪点）
        valid_vehicles = [cnt for cnt in contours if cv2.contourArea(cnt) > MIN_VEHICLE_AREA]

        return valid_vehicles, eroded