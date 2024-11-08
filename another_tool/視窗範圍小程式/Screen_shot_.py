import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab, ImageTk
import pyautogui
import os

class RegionSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("設定截圖範圍")
        
        # 建立 GUI 元件
        self.create_widgets()
    
    def create_widgets(self):
        # 顯示螢幕解析度按鈕
        button_screen_size = tk.Button(self.root, text="顯示螢幕解析度", command=self.get_screen_size)
        button_screen_size.grid(row=0, column=0, columnspan=2, pady=10)

        # 輸入截圖範圍
        tk.Label(self.root, text="左上角 X:").grid(row=1, column=0)
        self.entry_x = tk.Entry(self.root)
        self.entry_x.grid(row=1, column=1)

        tk.Label(self.root, text="左上角 Y:").grid(row=2, column=0)
        self.entry_y = tk.Entry(self.root)
        self.entry_y.grid(row=2, column=1)

        tk.Label(self.root, text="寬度:").grid(row=3, column=0)
        self.entry_width = tk.Entry(self.root)
        self.entry_width.grid(row=3, column=1)

        tk.Label(self.root, text="高度:").grid(row=4, column=0)
        self.entry_height = tk.Entry(self.root)
        self.entry_height.grid(row=4, column=1)

        # 預覽和儲存範圍按鈕
        button_preview = tk.Button(self.root, text="預覽範圍", command=self.preview_region)
        button_preview.grid(row=5, column=0, pady=10)

        button_save = tk.Button(self.root, text="儲存截圖範圍", command=self.save_region)
        button_save.grid(row=5, column=1, pady=10)

    def get_screen_size(self):
        # 獲取螢幕的解析度
        screen_width, screen_height = pyautogui.size()
        messagebox.showinfo("螢幕解析度", f"螢幕解析度為：{screen_width} x {screen_height}")

    def preview_region(self):
        try:
            x = int(self.entry_x.get())
            y = int(self.entry_y.get())
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
            
            # 檢查範圍是否在螢幕解析度內
            screen_width, screen_height = pyautogui.size()
            if x + width > screen_width or y + height > screen_height:
                messagebox.showerror("錯誤", "範圍超出螢幕解析度，請重新輸入")
            else:
                # 截取並顯示範圍的預覽圖
                screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
                screenshot.show()
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字")

    def save_region(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        joint_path = os.path.join(directory, "config.txt")
        try:
            x = int(self.entry_x.get())
            y = int(self.entry_y.get())
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
            
            # 檢查範圍是否在螢幕解析度內
            screen_width, screen_height = pyautogui.size()
            if x + width > screen_width or y + height > screen_height:
                messagebox.showerror("錯誤", "範圍超出螢幕解析度，請重新輸入")
            else:
                # 將截圖範圍保存至設定檔案
                with open(joint_path, "w") as f:
                    f.write(f"{x},{y},{width},{height}")
                messagebox.showinfo("成功", f"截圖範圍已儲存：({x}, {y}, {width}, {height})")
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字")

# 啟動 Tkinter 視窗
root = tk.Tk()
app = RegionSelector(root)
root.mainloop()
