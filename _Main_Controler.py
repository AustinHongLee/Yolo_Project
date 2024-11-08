import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import random
import shutil

# 設置主目錄為當前文件所在目錄
base_folder = os.path.dirname(__file__)

# 定義資料夾路徑
raw_images_folder = os.path.join(base_folder, "raw_images")
annotations_folder = os.path.join(base_folder, "annotations")
train_folder = os.path.join(base_folder, "training_data")
val_folder = os.path.join(base_folder, "validation_data")
config_folder = os.path.join(base_folder, "config")
classes_file = os.path.join(config_folder, "classes.txt")
summary_file_path = os.path.join(config_folder, "dataset_summary.txt")
yaml_path = os.path.join(config_folder, "yolov5_config.yaml")
yolo_train_script = os.path.join(base_folder, "yolov5", "train.py")

class DataPreparationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Data Preparation")

        # Step 1 按鈕：檢查檔名一致性
        self.verify_button = tk.Button(root, text="Step 1: 檢查檔名一致性", command=self.verify_filenames)
        self.verify_button.pack(pady=10)

        # Step 2 按鈕：檢查 class_id 並分配數據
        self.split_button = tk.Button(root, text="Step 2: 分配訓練和驗證集", command=self.split_data)
        self.split_button.pack(pady=10)

        # Step 3 按鈕：生成 dataset_summary.txt
        self.summary_button = tk.Button(root, text="Step 3: 生成數據集摘要", command=self.generate_summary)
        self.summary_button.pack(pady=10)

        # Step 4 按鈕：生成 yolov5_config.yaml
        self.yaml_button = tk.Button(root, text="Step 4: 生成 yolov5_config.yaml", command=self.generate_yaml)
        self.yaml_button.pack(pady=10)

        # Step 5 按鈕：生成訓練參數文件
        self.train_button = tk.Button(root, text="Step 5: 生成訓練參數文件", command=self.start_training)
        self.train_button.pack(pady=10)

    # Step 1 檢查檔名一致性
    def verify_filenames(self):
        image_files = [f.replace(".png", "") for f in os.listdir(raw_images_folder) if f.endswith(".png") and f != "README.txt"]
        annotation_files = [f.replace(".txt", "") for f in os.listdir(annotations_folder) if f.endswith(".txt") and f != "README.txt"]

        missing_images = [f + ".txt" for f in annotation_files if f not in image_files]
        missing_annotations = [f + ".png" for f in image_files if f not in annotation_files]

        if not missing_images and not missing_annotations:
            messagebox.showinfo("檢查結果", "所有圖片和標註文件名稱一致！")
        else:
            result = ""
            if missing_images:
                result += f"缺少圖片對應的標註文件: {', '.join(missing_images)}\n"
            if missing_annotations:
                result += f"缺少標註對應的圖片文件: {', '.join(missing_annotations)}\n"
            messagebox.showwarning("檢查結果", result)

    # Step 2 分配數據並檢查 class_id
    def check_classes(self):
        existing_classes = {}
        with open(classes_file, "r") as f:
            for idx, line in enumerate(f):
                existing_classes[str(idx)] = line.strip()

        new_classes_needed = {}
        for annotation_file in os.listdir(annotations_folder):
            if annotation_file.endswith(".txt") and annotation_file != "README.txt":
                with open(os.path.join(annotations_folder, annotation_file), "r") as file:
                    for line in file:
                        parts = line.split()
                        if parts:
                            class_id = parts[0]
                            if class_id not in existing_classes and class_id not in new_classes_needed:
                                class_name = simpledialog.askstring("輸入類別名稱", f"請輸入 class_id {class_id} 的名稱:")
                                new_classes_needed[class_id] = class_name

        with open(classes_file, "a") as f:
            for class_id, class_name in sorted(new_classes_needed.items()):
                f.write(f"{class_name}\n")

    def split_data(self):
        self.check_classes()
        for folder in [train_folder, val_folder]:
            os.makedirs(folder, exist_ok=True)

        image_files = [f for f in os.listdir(raw_images_folder) if f.endswith(".png")]
        train_ratio = 0.8
        train_size = int(len(image_files) * train_ratio)
        train_files = random.sample(image_files, train_size)
        val_files = [f for f in image_files if f not in train_files]

        for file_name in train_files:
            src_image_path = os.path.join(raw_images_folder, file_name)
            dest_image_path = os.path.join(train_folder, file_name)
            shutil.move(src_image_path, dest_image_path)
            label_file = file_name.replace(".png", ".txt")
            src_label_path = os.path.join(annotations_folder, label_file)
            dest_label_path = os.path.join(train_folder, label_file)
            shutil.move(src_label_path, dest_label_path)

        for file_name in val_files:
            src_image_path = os.path.join(raw_images_folder, file_name)
            dest_image_path = os.path.join(val_folder, file_name)
            shutil.move(src_image_path, dest_image_path)
            label_file = file_name.replace(".png", ".txt")
            src_label_path = os.path.join(annotations_folder, label_file)
            dest_label_path = os.path.join(val_folder, label_file)
            shutil.move(src_label_path, dest_label_path)

        messagebox.showinfo("完成", "資料分配完成！")

    # Step 3 生成數據集摘要
    def generate_summary(self):
        class_counts = {}
        with open(classes_file, "r") as f:
            classes = [line.strip() for line in f]
        
        for label_folder in [train_folder, val_folder]:
            for label_file in os.listdir(label_folder):
                if label_file.endswith(".txt"):
                    with open(os.path.join(label_folder, label_file), "r") as file:
                        for line in file:
                            try:
                                class_id = int(line.split()[0])
                                class_name = classes[class_id]
                                if class_name not in class_counts:
                                    class_counts[class_name] = 0
                                class_counts[class_name] += 1
                            except (IndexError, ValueError):
                                continue

        with open(summary_file_path, "w") as summary_file:
            total_images = len(os.listdir(train_folder)) + len(os.listdir(val_folder))
            summary_file.write("Dataset Summary\n")
            summary_file.write("------------------------\n")
            summary_file.write(f"Total images: {total_images}\n")
            summary_file.write(f"Training images: {len(os.listdir(train_folder))}\n")
            summary_file.write(f"Validation images: {len(os.listdir(val_folder))}\n\n")

            summary_file.write("Classes and Counts:\n")
            for class_id, class_name in enumerate(classes):
                count = class_counts.get(class_name, 0)
                summary_file.write(f"- Class {class_id} ({class_name}): {count} instances\n")

        messagebox.showinfo("完成", "dataset_summary.txt 已生成！")

    # Step 4 生成 yolov5_config.yaml
    def generate_yaml(self):
        try:
            if os.path.exists(yaml_path):
                overwrite = messagebox.askyesno("覆蓋文件", "yolov5_config.yaml 已存在。是否要覆蓋？")
                if not overwrite:
                    return
            
            with open(classes_file, "r") as f:
                classes = [line.strip() for line in f]
            num_classes = len(classes)

            with open(yaml_path, "w") as yaml_file:
                yaml_file.write("# YOLOv5 配置文件\n\n")
                yaml_file.write(f"path: {base_folder.replace(os.sep, '/')}\n")
                yaml_file.write("train: training_data\n")
                yaml_file.write("val: validation_data\n\n")
                yaml_file.write(f"nc: {num_classes}\n\n")
                yaml_file.write("names:\n")
                for class_name in classes:
                    yaml_file.write(f"  - {class_name}\n")
                
            messagebox.showinfo("完成", "yolov5_config.yaml 已生成！")

        except Exception as e:
            messagebox.showerror("錯誤", f"生成 yaml 文件時出現錯誤: {e}")

    # Step 5 生成訓練參數文件
    def start_training(self):
        img_size = 640
        batch_size = 16
        epochs = 50
        train_name = "yolo_training"

        img_size = simpledialog.askinteger("圖片大小", "請輸入圖片大小 (--img):", initialvalue=img_size)
        batch_size = simpledialog.askinteger("批次大小", "請輸入批次大小 (--batch):", initialvalue=batch_size)
        epochs = simpledialog.askinteger("訓練輪次", "請輸入訓練輪次 (--epochs):", initialvalue=epochs)
        train_name = simpledialog.askstring("訓練名稱", "請輸入訓練名稱 (--name):", initialvalue=train_name)

        try:
            params_file_path = os.path.join(config_folder, "training_params.txt")
            with open(params_file_path, "w") as params_file:
                params_file.write("Training Command\n")
                params_file.write("------------------------\n")
                params_file.write("執行以下命令來啟動訓練：\n\n")
                command = (
                    f"python {yolo_train_script} --img {img_size} --batch {batch_size} --epochs {epochs} "
                    f"--data {yaml_path} --weights yolov5s.pt --name {train_name} --verbose\n"
                )
                params_file.write(command)
            
            messagebox.showinfo("完成", "訓練參數文件已生成！請自行執行該命令進行訓練。")

        except Exception as e:
            messagebox.showerror("錯誤", f"生成訓練參數文件時出現錯誤: {e}")

# 建立 Tkinter 視窗
root = tk.Tk()
app = DataPreparationApp(root)
root.mainloop()
