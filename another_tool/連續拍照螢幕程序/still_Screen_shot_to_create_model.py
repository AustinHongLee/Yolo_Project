import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageGrab
import pyautogui
import time
import threading
import os

# 設定參數
DEFAULT_INTERVAL = 5  # 預設拍攝間隔（秒）
SCREEN_REGION = (0, 0, 2560, 1600)  # 預設截圖範圍 (x, y, 寬度, 高度)
DEFAULT_SAVING_FOLDER = r"G:\我的雲端硬碟\Python_Tool-main\OpenCV\Yolo\Project_Pratice_yolo1\raw_images"  # 預設儲存資料夾

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot App")
        self.interval = DEFAULT_INTERVAL  # 拍攝間隔
        self.saving_folder = DEFAULT_SAVING_FOLDER
        self.running = False

        # 建立 GUI 元件
        self.label = tk.Label(root, text="設定拍攝間隔 (秒):")
        self.label.pack()

        self.interval_entry = tk.Entry(root)
        self.interval_entry.insert(0, str(DEFAULT_INTERVAL))  # 預設間隔
        self.interval_entry.pack()

        self.select_folder_button = tk.Button(root, text="選擇儲存資料夾", command=self.select_folder)
        self.select_folder_button.pack()
        
        self.folder_label = tk.Label(root, text=f"儲存至: {self.saving_folder}")
        self.folder_label.pack()

        self.start_button = tk.Button(root, text="開始拍攝", command=self.start_screenshot)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="停止拍攝", command=self.stop_screenshot, state=tk.DISABLED)
        self.stop_button.pack()

    def select_folder(self):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            self.saving_folder = selected_folder
            self.folder_label.config(text=f"儲存至: {self.saving_folder}")

    def start_screenshot(self):
        if self.saving_folder:
            try:
                self.interval = int(self.interval_entry.get())
            except ValueError:
                messagebox.showerror("錯誤", "請輸入有效的數字作為間隔秒數")
                return
            
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            threading.Thread(target=self.screenshot_loop).start()
        else:
            messagebox.showerror("錯誤", "請先選擇儲存資料夾！")

    def stop_screenshot(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def screenshot_loop(self):
        while self.running:
            screenshot = pyautogui.screenshot(region=SCREEN_REGION)  # 使用設定的截圖範圍
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(self.saving_folder, f"screenshot_{timestamp}.png")
            screenshot.save(file_path)
            print(f"已儲存截圖: {file_path}")
            time.sleep(self.interval)

# 建立 Tkinter 視窗
root = tk.Tk()
app = ScreenshotApp(root)
root.mainloop()
