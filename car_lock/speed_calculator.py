#车速计算
import time
from config import PIXEL_PER_METER, DETECTION_LINE1_Y, DETECTION_LINE2_Y

class SpeedCalculator:
    def __init__(self):
        # 存储车辆通过第一条检测线的时间（key：车辆轮廓ID，value：时间戳）
        self.vehicle_pass_time = {}
        self.vehicle_id = 0  # 车辆唯一ID（自增）

    def calculate_speed(self, vehicle_contour, fps):
        """
        输入：车辆轮廓、视频帧率
        输出：车速（km/h，未通过两条线则返回None）
        """
        # 1. 获取车辆轮廓中心Y坐标（判断是否通过检测线）
        x, y, w, h = cv2.boundingRect(vehicle_contour)
        vehicle_center_y = y + h // 2

        # 2. 检测是否通过第一条线（记录时间）
        if DETECTION_LINE1_Y - 10 < vehicle_center_y < DETECTION_LINE1_Y + 10:
            self.vehicle_pass_time[self.vehicle_id] = time.time()
            self.vehicle_id += 1  # 下一辆车ID自增
            return None

        # 3. 检测是否通过第二条线（计算时间差）
        if DETECTION_LINE2_Y - 10 < vehicle_center_y < DETECTION_LINE2_Y + 10:
            # 查找当前车辆对应的第一条线通过时间
            for vid, pass_time in list(self.vehicle_pass_time.items()):
                # 计算两条线之间的像素距离
                pixel_distance = abs(DETECTION_LINE2_Y - DETECTION_LINE1_Y)
                # 时间差（秒）= 帧数差 / 帧率（简化计算：假设每帧间隔1/fps）
                time_diff = 1 / fps * len(self.vehicle_pass_time)  # 优化：实际可跟踪帧号
                if time_diff <= 0:
                    continue

                # 4. 计算实际速度：km/h = (米 / 秒) * 3.6
                meter_distance = pixel_distance / PIXEL_PER_METER  # 像素转实际距离（米）
                speed_mps = meter_distance / time_diff  # 米/秒
                speed_kmh = round(speed_mps * 3.6, 1)  # 转换为km/h

                # 移除已计算速度的车辆记录（避免重复计算）
                del self.vehicle_pass_time[vid]
                return speed_kmh

        return None  # 未完成两条线检测，暂不返回速度