#工具函数
import cv2
from config import (
    LINE_COLOR, LINE_THICKNESS, DETECTION_LINE1_Y, DETECTION_LINE2_Y,
    TEXT_FONT, TEXT_SIZE, TEXT_COLOR, TEXT_THICKNESS, FRAME_WIDTH
)


def draw_detection_lines(frame):
    """在帧上绘制两条测速检测线"""
    # 第一条线（上）
    cv2.line(
        frame, (0, DETECTION_LINE1_Y), (FRAME_WIDTH, DETECTION_LINE1_Y),
        LINE_COLOR, LINE_THICKNESS
    )
    cv2.putText(
        frame, "Line 1", (10, DETECTION_LINE1_Y - 10),
        TEXT_FONT, TEXT_SIZE, LINE_COLOR, TEXT_THICKNESS
    )

    # 第二条线（下）
    cv2.line(
        frame, (0, DETECTION_LINE2_Y), (FRAME_WIDTH, DETECTION_LINE2_Y),
        LINE_COLOR, LINE_THICKNESS
    )
    cv2.putText(
        frame, "Line 2", (10, DETECTION_LINE2_Y - 10),
        TEXT_FONT, TEXT_SIZE, LINE_COLOR, TEXT_THICKNESS
    )
    return frame


def draw_vehicle_info(frame, vehicle_contour, license_plate, speed):
    """在帧上绘制车辆轮廓、车牌、车速"""
    x, y, w, h = cv2.boundingRect(vehicle_contour)

    # 绘制车辆边框
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # 绘制车牌（若识别到）
    if license_plate:
        cv2.putText(
            frame, f"Plate: {license_plate}", (x, y - 30),
            TEXT_FONT, TEXT_SIZE, TEXT_COLOR, TEXT_THICKNESS
        )

    # 绘制车速（若计算出）
    if speed is not None:
        speed_text = f"Speed: {speed} km/h"
        cv2.putText(
            frame, speed_text, (x, y - 10),
            TEXT_FONT, TEXT_SIZE, (0, 255, 255), TEXT_THICKNESS  # 黄色文字
        )
    return frame