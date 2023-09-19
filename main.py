import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
import os
import subprocess
import datetime


# building main windows
class App:
    def __init__(self):
        # mainwindows la 1 thuoc tinh cua lop app
        self.main_windows = tk.Tk()
        # tao ra 1 cua so chinh cua ung dung GUI
        self.main_windows.geometry("1200x520+350+100")
        # tao 1 cua so chinh co kich thuoc 1200*520 cach tren 100 , cach ben trai 350

        # tao 1 nut co chieu dai 20 , cao 2 ,nam tai x=750 , y =300
        self.login_button_main_window = util.get_button(
            self.main_windows, "login", "green", self.login
        )
        self.login_button_main_window.place(x=750, y=300)

        # tao 1 nut co chieu dai 20 , cao 2 , text register, nam tai x=750,y=400
        self.register_new_user_button_main_window = util.get_button(
            self.main_windows,
            "register new user ",
            "gray",
            self.register_new_user,
            fg="black",
        )
        self.register_new_user_button_main_window.place(x=750, y=400)
        # tao 1 cai nhan dan
        self.webcam_label = util.get_img_label(self.main_windows)
        # tao 1 nhan co chieu dai 700 , chieu cao 500
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = "./db"
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = "/.log.txt"

    def add_webcam(self, label):
        if "cap" not in self.__dict__:
            # Kiểm tra xem thuộc tính cap có được định nghĩa trong đối tượng App không
            # Nếu cap chưa tồn tại, tạo một đối tượng VideoCapture để truy cập webcam
            self.cap = cv2.VideoCapture(0)

        self._label = label

        self.process_webcam()

    def process_webcam(self):
        # Đọc một khung hình từ webcam.
        ret, frame = self.cap.read()
        # luu khung hinh trong bien self.most_recent_capture_arr
        self.most_recent_capture_arr = frame
        # Chuyển đổi màu của hình ảnh từ BGR (sử dụng bởi OpenCV) sang RGB
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

        # Tạo một đối tượng hình ảnh từ mảng NumPy (img_) với Pillow (PIL).
        self.most_recent_capture_pil = Image.fromarray(img_)
        # Tạo một đối tượng tkinter PhotoImage từ hình ảnh.
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        # Cập nhật hình ảnh trong nhãn để hiển thị khung hình từ webcam.
        self._label.imgtk = imgtk
        # Cập nhật hình ảnh trong nhãn để hiển thị khung hình từ webcam.
        self._label.configure(image=imgtk)

        self._label.after(10, self.process_webcam)

    def login(self):
        unknow_img_path = "./.tmp.jpg"

        cv2.imwrite(unknow_img_path, self.most_recent_capture_arr)

        output = str(
            subprocess.check_output(["face_recognition", self.db_dir, unknow_img_path])
        )

        name = output.split(",")[1][:-5]
        if name in ["no_persons_found", "unknown_person"]:
            util.msg_box("Ups...", "Unknow user.pls,register new User or  try again")
        else:
            util.msg_box("Welcome back!", "Welcome .{}".format(name))

            with open(self.log_path, "a") as f:
                f.write("{}", "{}\n".format(name, datetime.datetime.now()))
                f.close()

        os.remove(unknow_img_path)

    def register_new_user(self):
        self.register_new_user_windows = tk.Toplevel(self.main_windows)
        self.register_new_user_windows.geometry("1200x520+370+120")
        self.accept_button_register_new_user_windows = util.get_button(
            self.register_new_user_windows,
            "Accept",
            "green",
            self.accept_register_new_user,
        )
        self.accept_button_register_new_user_windows.place(x=750, y=300)

        self.try_again_button_register_new_user_windows = util.get_button(
            self.register_new_user_windows,
            "Try Again",
            "red",
            self.try_again_register_new_user,
        )
        self.try_again_button_register_new_user_windows.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_windows)
        # tao 1 nhan co chieu dai 700 , chieu cao 500
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(
            self.register_new_user_windows
        )
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(
            self.register_new_user_windows, "Pls,\ninput userName:"
        )
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_windows.destroy()

    def add_img_to_label(self, lable):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        # Cập nhật hình ảnh trong nhãn để hiển thị khung hình từ webcam.
        lable.imgtk = imgtk
        # Cập nhật hình ảnh trong nhãn để hiển thị khung hình từ webcam.
        lable.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def Start(self):
        # Gọi vòng lặp sự kiện chính để các hành động có thể diễn ra trên màn hình máy tính của người dùng
        self.main_windows.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        cv2.imwrite(
            os.path.join(self.db_dir, "{}.jpg".format(name)),
            self.register_new_user_capture,
        )
        util.msg_box("Success", "User was registered succesfully!")

        self.register_new_user_windows.destroy()


if __name__ == "__main__":
    app = App()
    app.Start()
