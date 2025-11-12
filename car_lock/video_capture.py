#视频流读取
import cv2
from config import VIDEO_SOURCE, FPS, FRAME_WIDTH, FRAME_HEIGHT


class VideoCapture:
    def __init__(self):
        # 初始化视频捕获（摄像头/本地视频）
        self.cap = cv2.VideoCapture(VIDEO_SOURCE)
        if not self.cap.isOpened():
            raise ValueError(f"无法打开视频源：{VIDEO_SOURCE}")

        # 获取实际视频帧率（若失败则用默认值）
        self.actual_fps = self.cap.get(cv2.CAP_PROP_FPS) or FPS
        self.frame_width = FRAME_WIDTH
        self.frame_height = FRAME_HEIGHT

    def read_frame(self):
        """读取一帧并调整分辨率"""
        ret, frame = self.cap.read()
        if not ret:
            return False, None  # 视频结束或读取失败

        # 调整帧大小（统一分辨率）
        frame_resized = cv2.resize(frame, (self.frame_width, self.frame_height))
        return True, frame_resized

    def release(self):
        """释放视频资源"""
        self.cap.release()
        cv2.destroyAllWindows()

    def get_fps(self):
        """获取视频帧率（用于测速计算）"""
        return self.actual_fps