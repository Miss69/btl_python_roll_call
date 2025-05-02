from backend.utils.face_detection import FaceDetectionAPI
import cv2
import numpy as np

class FaceService:
    def __init__(self):
        self.api = FaceDetectionAPI()
    
    async def register_face(self, employee_id: int, image_data: bytes) -> bool:
        """
        Đăng ký khuôn mặt mới
        Args:
            employee_id: ID của nhân viên
            image_data: Dữ liệu ảnh dưới dạng bytes
        Returns:
            bool: True nếu đăng ký thành công
        """
        # Chuyển đổi dữ liệu ảnh
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Phát hiện khuôn mặt
        success, face_img = self.api.detect_face(img)
        if not success:
            return False
        
        # Lưu khuôn mặt
        return self.api.register_face(employee_id, face_img)
    
    async def recognize_face(self, image_data: bytes) -> int:
        """
        Nhận diện khuôn mặt
        Args:
            image_data: Dữ liệu ảnh dưới dạng bytes
        Returns:
            int: ID của nhân viên nếu tìm thấy
        """
        # Chuyển đổi dữ liệu ảnh
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Phát hiện khuôn mặt
        success, face_img = self.api.detect_face(img)
        if not success:
            return None
        
        # Nhận diện khuôn mặt
        return self.api.recognize_face(face_img) 