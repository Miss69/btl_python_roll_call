import cv2
import numpy as np
from typing import Tuple, Optional, Dict, Any
import os

class FaceDetectionAPI:
    def __init__(self):
        # TODO: Khởi tạo các tham số cần thiết cho API AI
        # Ví dụ: API key, endpoint, model path, etc.
        self.api_key = None
        self.endpoint = None
        self.model_path = None
        
        # Thư mục lưu trữ ảnh nhân viên
        self.EMPLOYEE_IMAGES_DIR = "employee_images"
        
        # Tạo thư mục nếu chưa tồn tại
        if not os.path.exists(self.EMPLOYEE_IMAGES_DIR):
            os.makedirs(self.EMPLOYEE_IMAGES_DIR)
    
    def detect_face(self, image: np.ndarray) -> Tuple[bool, np.ndarray]:
        """
        Phát hiện khuôn mặt trong ảnh sử dụng API AI
        Args:
            image: Ảnh đầu vào dưới dạng numpy array
        Returns:
            Tuple[bool, np.ndarray]: (có tìm thấy khuôn mặt, ảnh đã được cắt)
        """
        # TODO: Gọi API AI để phát hiện khuôn mặt
        # Ví dụ:
        # response = self._call_api('detect', image)
        # if response['success']:
        #     face_box = response['face_box']
        #     x, y, w, h = face_box
        #     face_img = image[y:y+h, x:x+w]
        #     return True, face_img
        # return False, None
        
        # Tạm thời sử dụng OpenCV
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            return False, None
        
        (x, y, w, h) = faces[0]
        face_img = image[y:y+h, x:x+w]
        return True, face_img
    
    def recognize_face(self, face_img: np.ndarray) -> Optional[int]:
        """
        Nhận diện khuôn mặt sử dụng API AI
        Args:
            face_img: Ảnh khuôn mặt đã được cắt
        Returns:
            Optional[int]: ID của nhân viên nếu tìm thấy, None nếu không tìm thấy
        """
        # TODO: Gọi API AI để nhận diện khuôn mặt
        # Ví dụ:
        # response = self._call_api('recognize', face_img)
        # if response['success']:
        #     return response['employee_id']
        # return None
        
        # Tạm thời sử dụng template matching
        face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        best_match_id = None
        best_match_score = 0
        
        for filename in os.listdir(self.EMPLOYEE_IMAGES_DIR):
            if filename.endswith(".jpg"):
                employee_id = int(filename.split(".")[0])
                saved_img = cv2.imread(os.path.join(self.EMPLOYEE_IMAGES_DIR, filename))
                saved_gray = cv2.cvtColor(saved_img, cv2.COLOR_BGR2GRAY)
                
                # Resize ảnh về cùng kích thước
                saved_gray = cv2.resize(saved_gray, (face_gray.shape[1], face_gray.shape[0]))
                
                # Tính độ tương đồng
                result = cv2.matchTemplate(face_gray, saved_gray, cv2.TM_CCOEFF_NORMED)
                score = cv2.minMaxLoc(result)[1]
                
                if score > best_match_score:
                    best_match_score = score
                    best_match_id = employee_id
        
        if best_match_score > 0.7:
            return best_match_id
        return None
    
    def register_face(self, employee_id: int, face_img: np.ndarray) -> bool:
        """
        Đăng ký khuôn mặt mới sử dụng API AI
        Args:
            employee_id: ID của nhân viên
            face_img: Ảnh khuôn mặt đã được cắt
        Returns:
            bool: True nếu đăng ký thành công, False nếu thất bại
        """
        # TODO: Gọi API AI để đăng ký khuôn mặt
        # Ví dụ:
        # response = self._call_api('register', face_img, employee_id)
        # return response['success']
        
        # Tạm thời lưu ảnh vào thư mục
        try:
            filename = f"{employee_id}.jpg"
            filepath = os.path.join(self.EMPLOYEE_IMAGES_DIR, filename)
            cv2.imwrite(filepath, face_img)
            return True
        except Exception as e:
            print(f"Error saving face: {str(e)}")
            return False
    
    def _call_api(self, endpoint: str, image: np.ndarray, *args) -> Dict[str, Any]:
        """
        Gọi API AI
        Args:
            endpoint: Tên endpoint của API
            image: Ảnh đầu vào
            *args: Các tham số bổ sung
        Returns:
            Dict[str, Any]: Kết quả từ API
        """
        # TODO: Implement logic gọi API AI
        # Ví dụ:
        # headers = {'Authorization': f'Bearer {self.api_key}'}
        # files = {'image': ('image.jpg', cv2.imencode('.jpg', image)[1].tobytes())}
        # response = requests.post(f"{self.endpoint}/{endpoint}", headers=headers, files=files, data=args)
        # return response.json()
        pass
