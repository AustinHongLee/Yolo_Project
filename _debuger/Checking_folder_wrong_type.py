import os
from PIL import Image

base_path = r"G:\我的雲端硬碟\Python_Tool-main\OpenCV\Yolo\Project_Pratice_yolo1"

expected_extensions = {
    "raw_images": {".png", ".jpg", ".jpeg"},
    "annotations": {".txt"},
    "reviewed_annotations": {".txt"},
    "augmented_data/augmented_images": {".png", ".jpg", ".jpeg"},
    "augmented_data/augmented_labels": {".txt"},
    "training_data/train_images": {".png", ".jpg", ".jpeg"},
    "training_data/train_labels": {".txt"},
    "validation_data/val_images": {".png", ".jpg", ".jpeg"},
    "validation_data/val_labels": {".txt"},
    "model_outputs": {".pth"},
    "config": {".txt", ".yaml"},
    "requirements.txt": {".txt"}
}

# 類別檢查 - 讀取 classes.txt 類別
def load_classes():
    classes_path = os.path.join(base_path, "config", "classes.txt")
    if os.path.exists(classes_path):
        with open(classes_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

# 檢查非預期文件、文件一致性、格式及內容
def check_data_integrity():
    unexpected_files = []
    missing_annotations = []
    invalid_annotations = []
    empty_annotations = []
    inconsistent_images = []
    empty_folders = []
    classes = load_classes()

    for folder, extensions in expected_extensions.items():
        folder_path = os.path.join(base_path, folder)

        if not os.path.exists(folder_path):
            print(f"資料夾 {folder_path} 不存在，跳過檢查。")
            continue

        files_in_folder = list(os.walk(folder_path))[0][2]
        if not files_in_folder:
            empty_folders.append(folder_path)
            continue

        for file in files_in_folder:
            file_path = os.path.join(folder_path, file)
            file_ext = os.path.splitext(file)[1].lower()
            
            # 檢查文件副檔名
            if file_ext not in extensions:
                unexpected_files.append(file_path)

            # 檢查標註文件格式
            if folder.endswith("labels") and file_ext == ".txt":
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    if not lines:
                        empty_annotations.append(file_path)
                    for line in lines:
                        parts = line.strip().split()
                        if len(parts) != 5 or not all(0 <= float(num) <= 1 for num in parts[1:]):
                            invalid_annotations.append(file_path)
                        elif parts[0] not in classes:
                            invalid_annotations.append(file_path)

            # 檢查圖片解析度一致性
            if folder.endswith("images") and file_ext in {".png", ".jpg", ".jpeg"}:
                with Image.open(file_path) as img:
                    if img.size != (640, 640):  # 假設期望解析度為 640x640
                        inconsistent_images.append(file_path)

    # 輸出結果
    print("檢查結果:")
    if empty_folders:
        print("\n空的資料夾:")
        for folder in empty_folders:
            print(folder)

    if unexpected_files:
        print("\n非預期文件:")
        for file in unexpected_files:
            print(file)

    if missing_annotations:
        print("\n缺少標註的圖像:")
        for file in missing_annotations:
            print(file)

    if empty_annotations:
        print("\n空的標註文件:")
        for file in empty_annotations:
            print(file)

    if invalid_annotations:
        print("\n無效的標註文件:")
        for file in invalid_annotations:
            print(file)

    if inconsistent_images:
        print("\n解析度不一致的圖像:")
        for file in inconsistent_images:
            print(file)

    if not (empty_folders or unexpected_files or missing_annotations or empty_annotations or invalid_annotations or inconsistent_images):
        print("所有文件均符合預期格式和要求。")

# 執行檢查
if __name__ == "__main__":
    check_data_integrity()
