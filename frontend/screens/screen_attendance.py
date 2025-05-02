import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import cv2

# Cấu hình thư viện customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AttendanceScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        self.controller = controller  # Lưu controller để sử dụng sau này
        
        # Biến để lưu trạng thái camera
        self.camera = None
        self.is_camera_running = False
        
        # Nút quay lại
        back_button = ctk.CTkButton(
            self,
            text="Quay lại",
            command=self.controller.show_home,
            font=("Arial", 12, "bold"),
            fg_color="#000080",
            width=100,
            height=30
        )
        back_button.pack(anchor="nw", padx=10, pady=10)
        
        # Tiêu đề - Có thể thay đổi màu chữ ở đây
        title_label = ctk.CTkLabel(self, text="Hệ thống chấm công khuôn mặt", 
                              font=("Arial", 24, "bold"), 
                              text_color="#FF0000")  # Thay đổi màu chữ ở đây
        title_label.pack(pady=10)

        # Frame chính chứa các phần tử
        main_frame = ctk.CTkFrame(self, fg_color="white")
        main_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # ==== PHẦN BÊN TRÁI ====
        left_frame = ctk.CTkFrame(main_frame, fg_color="white", border_width=2, border_color="gray")
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Frame cho phần nhận diện
        recognition_frame = ctk.CTkFrame(left_frame, fg_color="white", border_width=1, border_color="gray")
        recognition_frame.pack(fill="x", pady=10, padx=10)

        # Có thể thay đổi màu chữ ở đây
        recognition_label = ctk.CTkLabel(recognition_frame, text="Màn hình nhận diện", 
                                   font=("Arial", 12, "bold"),
                                   text_color="black")  # Thay đổi màu chữ ở đây
        recognition_label.pack(anchor="w", padx=10, pady=5)

        # Chọn loại chấm công
        frame_top = ctk.CTkFrame(recognition_frame, fg_color="white")
        frame_top.pack(pady=10, fill="x", padx=10)

        # Có thể thay đổi màu chữ ở đây
        type_label = ctk.CTkLabel(frame_top, text="Chọn loại Chấm công:", 
                             font=("Arial", 12),
                             text_color="black")  # Thay đổi màu chữ ở đây
        type_label.pack(side="left", padx=5)

        self.type_combobox = ctk.CTkComboBox(frame_top, values=["Check in", "Check out"], 
                                   width=300, height=30)
        self.type_combobox.pack(side="left", padx=5)

        # Khung danh sách nhận diện
        self.face_frame = ctk.CTkFrame(left_frame, fg_color="white", border_width=1, 
                             border_color="gray", width=640, height=480)  # Kích thước cố định
        self.face_frame.pack(padx=10, pady=10)
        self.face_frame.pack_propagate(False)  # Ngăn không cho frame tự động mở rộng
        
        # Thêm label để hiển thị camera
        self.camera_label = tk.Label(self.face_frame, bg="black")
        self.camera_label.pack(fill="both", expand=True)

        # Thông báo phía dưới - Có thể thay đổi màu chữ ở đây
        self.notice_label = ctk.CTkLabel(left_frame, 
                               text="Thông báo: Vui lòng chọn loại chấm công để mở Camera", 
                               text_color="#FF0000",  # Thay đổi màu chữ ở đây
                               font=("Arial", 11))
        self.notice_label.pack(pady=5)

        # Nút mở / đóng camera
        button_frame = ctk.CTkFrame(left_frame, fg_color="white")
        button_frame.pack(pady=5)

        # Tạo frame con để căn giữa các nút
        button_container = ctk.CTkFrame(button_frame, fg_color="white")
        button_container.pack(expand=True)

        self.start_button = ctk.CTkButton(button_container, text="Mở Camera",
                                font=("Arial", 12, "bold"),
                                fg_color="#000080", 
                                width=200,
                                height=35,
                                command=self.start_camera)
        self.start_button.pack(side="left", padx=(50, 20))

        self.stop_button = ctk.CTkButton(button_container, text="Đóng Camera",
                               font=("Arial", 12, "bold"),
                               fg_color="#000080",
                               width=200,
                               height=35,
                               command=self.stop_camera)
        self.stop_button.pack(side="left", padx=(20, 50))
        
        # Vô hiệu hóa nút đóng camera ban đầu
        self.stop_button.configure(state="disabled")

        # ==== PHẦN BÊN PHẢI ====
        right_frame = ctk.CTkFrame(main_frame, fg_color="white", border_width=2, border_color="gray")
        right_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Frame trên - Điểm danh thành công và thông tin nhân viên
        top_right_frame = ctk.CTkFrame(right_frame, fg_color="white", border_width=1, border_color="gray")
        top_right_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Có thể thay đổi màu chữ ở đây
        success_label = ctk.CTkLabel(top_right_frame, text="Chấm công thành công",
                                font=("Arial", 14, "bold"),
                                text_color="black")  # Thay đổi màu chữ ở đây
        success_label.pack(pady=10)

        # Khung hình ảnh khuôn mặt
        image_frame = ctk.CTkFrame(top_right_frame, fg_color="white", border_width=1, border_color="gray")
        image_frame.pack(pady=10, padx=10)

        # Load ảnh mặc định (dấu hỏi)
        default_image = Image.open("frontend/assets/default_avatar.png")
        default_image = default_image.resize((150, 150))
        self.photo = ImageTk.PhotoImage(default_image)
        self.img_label = ctk.CTkLabel(image_frame, image=self.photo, text="")
        self.img_label.pack(pady=5)

        # Thông tin nhân viên
        self.employee_info = {
            "id": "",
            "name": "",
            "time": ""
        }

        info_content = ctk.CTkFrame(top_right_frame, fg_color="white", border_width=1, border_color="gray")
        info_content.pack(fill="x", padx=10, pady=10)

        # Có thể thay đổi màu chữ ở đây
        self.id_label = ctk.CTkLabel(info_content, text="ID Nhân viên:", 
                                font=("Arial", 12),
                                text_color="black")  # Thay đổi màu chữ ở đây
        self.id_label.pack(anchor="w", padx=10, pady=5)

        # Có thể thay đổi màu chữ ở đây
        self.name_label = ctk.CTkLabel(info_content, text="Tên Nhân viên:", 
                                  font=("Arial", 12),
                                  text_color="black")  # Thay đổi màu chữ ở đây
        self.name_label.pack(anchor="w", padx=10, pady=5)

        # Có thể thay đổi màu chữ ở đây
        self.time_label = ctk.CTkLabel(info_content, text="Thời gian:", 
                                  font=("Arial", 12),
                                  text_color="black")  # Thay đổi màu chữ ở đây
        self.time_label.pack(anchor="w", padx=10, pady=5)

        # Frame dưới - Thông tin nhân viên
        bottom_right_frame = ctk.CTkFrame(right_frame, fg_color="white", border_width=1, border_color="gray")
        bottom_right_frame.pack(fill="both", padx=5, pady=5)

        # Có thể thay đổi màu chữ ở đây
        info_title = ctk.CTkLabel(bottom_right_frame, text="Thông tin nhân viên",
                               font=("Arial", 12, "bold"),
                               text_color="black")  # Thay đổi màu chữ ở đây
        info_title.pack(anchor="w", padx=10, pady=5)

        # Có thể thay đổi màu chữ ở đây
        self.dept_label = ctk.CTkLabel(bottom_right_frame, text="Phòng ban: ", 
                text_color="#FF0000",  # Thay đổi màu chữ ở đây
                font=("Arial", 12))
        self.dept_label.pack(anchor="w", padx=10)

        # Có thể thay đổi màu chữ ở đây
        self.position_label = ctk.CTkLabel(bottom_right_frame, text="Chức vụ: ", 
                text_color="#FF0000",  # Thay đổi màu chữ ở đây
                font=("Arial", 12))
        self.position_label.pack(anchor="w", padx=10)

        # Có thể thay đổi màu chữ ở đây
        self.checkin_time_label = ctk.CTkLabel(bottom_right_frame, text="Thời gian điểm danh: ", 
                text_color="#FF0000",  # Thay đổi màu chữ ở đây
                font=("Arial", 12))
        self.checkin_time_label.pack(anchor="w", padx=10, pady=(0,5))

    def format_time_range(self, check_time):
        """Tính toán và định dạng khoảng thời gian làm việc 8 tiếng"""
        # Chuyển đổi chuỗi thời gian thành đối tượng datetime
        start_time = datetime.strptime(check_time, "%H:%M:%S")
        # Cộng thêm 8 tiếng
        end_time = start_time + timedelta(hours=8)
        # Định dạng lại thành chuỗi
        return f"{start_time.strftime('%H:%M:%S')} - {end_time.strftime('%H:%M:%S')}"

    def update_employee_details(self, department, position, checkin_time):
        """Cập nhật thông tin chi tiết của nhân viên"""
        self.dept_label.configure(text=f"Phòng ban: {department}")
        self.position_label.configure(text=f"Chức vụ: {position}")
        # Hiển thị khoảng thời gian làm việc
        time_range = self.format_time_range(checkin_time)
        self.checkin_time_label.configure(text=f"Thời gian làm việc: {time_range}")

    def show_employee_info(self, employee_id, employee_name, check_time, department="", position=""):
        """Hiển thị thông tin nhân viên khi chấm công thành công"""
        # Cập nhật thông tin cơ bản
        self.employee_info["id"] = employee_id
        self.employee_info["name"] = employee_name
        self.employee_info["time"] = check_time
        
        # Cập nhật nội dung phần trên
        self.id_label.configure(text=f"ID Nhân viên: {employee_id}")
        self.name_label.configure(text=f"Tên Nhân viên: {employee_name}")
        self.time_label.configure(text=f"Thời gian: {check_time}")
        
        # Cập nhật thông tin chi tiết phần dưới
        self.update_employee_details(department, position, check_time)

    def start_camera(self):
        """Mở camera và bắt đầu hiển thị hình ảnh"""
        if not self.is_camera_running:
            self.camera = cv2.VideoCapture(0)
            self.is_camera_running = True
            
            # Cập nhật trạng thái nút
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            
            # Cập nhật thông báo
            self.notice_label.configure(text="Camera đang hoạt động", text_color="green")
            
            # Bắt đầu hiển thị hình ảnh từ camera
            self.show_camera_feed()

    def stop_camera(self):
        """Đóng camera và dừng hiển thị hình ảnh"""
        if self.is_camera_running:
            self.camera.release()
            self.is_camera_running = False
            
            # Cập nhật trạng thái nút
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            
            # Cập nhật thông báo
            self.notice_label.configure(text="Camera đã tắt", text_color="red")
            
            # Xóa hình ảnh hiện tại
            self.camera_label.configure(image="")

    def show_camera_feed(self):
        """Hiển thị hình ảnh từ camera"""
        if self.is_camera_running:
            ret, frame = self.camera.read()
            if ret:
                # Chuyển đổi frame từ BGR sang RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Thay đổi kích thước frame để phù hợp với khung hiển thị
                frame = cv2.resize(frame, (640, 480))  # Kích thước cố định
                
                # Chuyển đổi frame thành ảnh PIL
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image=image)
                
                # Hiển thị ảnh
                self.camera_label.configure(image=photo)
                self.camera_label.image = photo  # Giữ reference để tránh bị garbage collected
                
                # Cập nhật hình ảnh
                self.after(10, self.show_camera_feed)  # Cập nhật mỗi 10ms
            else:
                self.stop_camera()
                self.notice_label.configure(text="Không thể mở camera", text_color="red")

    def __del__(self):
        """Đảm bảo camera được đóng khi đối tượng bị hủy"""
        if self.camera is not None:
            self.camera.release()

