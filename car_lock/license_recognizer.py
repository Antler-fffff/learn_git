#车牌识别
import easyocr
import cv2
from config import OCR_LANG, OCR_CONFIDENCE


class LicensePlateRecognizer:
    def __init__(self):
        # 初始化EasyOCR阅读器（只初始化一次，提升效率）
        self.reader = easyocr.Reader(OCR_LANG, gpu=False)  # gpu=True需安装CUDA

    def recognize(self, frame, vehicle_contour):
        """
        输入：原始帧、车辆轮廓
        输出：车牌文本（无则返回None）
        """
        # 1. 获取车辆轮廓的 bounding box（定位车辆区域）
        x, y, w, h = cv2.boundingRect(vehicle_contour)

        # 2. 裁剪车辆区域（缩小识别范围，提升准确率）
        vehicle_roi = frame[y:y + h, x:x + w]

        # 3. 预处理：转换为灰度图+自适应阈值（增强车牌对比度）
        gray_roi = cv2.cvtColor(vehicle_roi, cv2.COLOR_BGR2GRAY)
        adaptive_thresh = cv2.adaptiveThreshold(
            gray_roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, blockSize=11, C=2
        )

        # 4. 车牌识别（EasyOCR核心）
        results = self.reader.readtext(adaptive_thresh)

        # 5. 过滤低置信度结果，提取车牌文本
        for (bbox, text, confidence) in results:
            if confidence >= OCR_CONFIDENCE and len(text) >= 7:  # 车牌长度至少7位（如粤A12345）
                return text.strip()

        return None  # 未识别到车牌