G:\我的雲端硬碟\Python_Tool-main\OpenCV\Yolo\Project_Pratice_yolo1                         # 主專案資料夾
│
├── raw_images                    # [必要] 原始設計圖及截圖，作為訓練數據的來源
│
├── annotations                   # [必要] 標註文件，描述目標位置和類別
│
├── reviewed_annotations          # [非必要] 檢查後無誤的標註文件，避免訓練時的錯誤
│
├── augmented_data                # [非必要] 數據增強資料
│   ├── augmented_images          # 增強後的圖像資料
│   └── augmented_labels          # 增強後的標註文件
│
├── training_data                 # [必要] 用於模型訓練的數據集合
│   ├── train_images              # 訓練集的圖片
│   └── train_labels              # 訓練集的標註文件
│
├── validation_data               # [必要] 用於模型驗證的數據集合
│   ├── val_images                # 驗證集的圖片
│   └── val_labels                # 驗證集的標註文件
│
├── model_outputs                 # [必要] 訓練後的模型文件
│
├── config                        # [必要] 訓練配置
│   ├── classes.txt               # 類別名稱檔案，記錄模型識別的類別
│   ├── yolov5_config.yaml        # YOLO 模型配置文件（或 cfg 文件）
│   └── dataset_summary.txt       # [非必要] 數據集摘要報告，顯示數據集統計資訊
│
└── requirements.txt              # [非必要] 訓練環境依賴項，便於快速設置環境
