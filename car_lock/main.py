import cv2
from video_capture import VideoCapture
from vehicle_detector import VehicleDetector
from license_recognizer import LicensePlateRecognizer
from speed_calculator import SpeedCalculator
from utils import draw_detection_lines, draw_vehicle_info

def main():
    # 初始化所有模块
    print("初始化模块...")
    video_capture = VideoCapture()
    vehicle_detector = VehicleDetector()
    license_recognizer = LicensePlateRecognizer()
    speed_calculator = SpeedCalculator()
    fps = video_capture.get_fps()
    print(f"视频帧率：{fps:.1f} FPS")

    try:
        print("开始检测（按 'q' 退出）...")
        while True:
            # 1. 读取视频帧
            ret, frame = video_capture.read_frame()
            if not ret:
                print("视频读取完毕或出错！")
                break

            # 2. 绘制测速检测线
            frame_with_lines = draw_detection_lines(frame.copy())

            # 3. 检测车辆
            vehicles, fg_mask = vehicle_detector.detect_vehicles(frame)

            # 4. 遍历每辆车，识别车牌+计算车速
            for vehicle in vehicles:
                # 识别车牌
                license_plate = license_recognizer.recognize(frame, vehicle)
                # 计算车速
                speed = speed_calculator.calculate_speed(vehicle, fps)
                # 绘制车辆信息
                frame_with_lines = draw_vehicle_info(frame_with_lines, vehicle, license_plate, speed)

            # 5. 显示结果（原始帧+检测结果）
            cv2.imshow("License Plate + Speed Detection", frame_with_lines)
            cv2.imshow("Foreground Mask", fg_mask)  # 前景掩码（可选显示）

            # 按 'q' 退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"程序出错：{str(e)}")
    finally:
        # 释放资源
        video_capture.release()
        print("程序退出，资源已释放！")

if __name__ == "__main__":
    main()