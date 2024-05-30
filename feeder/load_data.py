import os
import re
import json
# import xlrd
import numpy as np
import pandas as pd
# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2

def extract_info(s):
    # 使用正则表达式提取日期和后缀
    match = re.search(r'(\d{8})_([A-Z]+)_\d', s)
    if match:
        # 提取日期和后缀
        date, suffix = match.groups()
        return date, suffix
    else:
        return None, None

def compare_strings(s1, s2):  
    # 提取两个字符串的信息
    date1, suffix1 = extract_info(s1)
    date2, suffix2 = extract_info(s2)

    # 比较日期和后缀
    return (date1 == date2) and (suffix1 == suffix2)

def OnePatient (path):

    patient = np.empty( (0, 25, 3) )
    file_list = os.listdir(path)

    for file_name in file_list:
        # 檢查檔案是否為 JSON 檔案
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as json_file:
                try:
                    # 讀取 JSON 檔案內容
                    data = json.load(json_file)    
                    # 在這裡可以對讀取的 JSON 資料進行處理
                    keypoints = np.array(data['people'][0]['pose_keypoints_2d']).reshape(-1, 3)
                    # leg = keypoints[8:15]
                    # leg = leg.flatten()
                    # leg = np.expand_dims (leg, axis=0)
                    # patient = np.append (patient, leg, axis=0)                
                    patient = patient [:700, :]
                    
                except json.JSONDecodeError as e:
                    print(f"Error reading JSON file {file_name}: {e}")

    return patient
    

def process_json_files(root_dir, patients):
    """
    從指定的根目錄中遍歷並處理所有JSON檔案。

    Parameters:
    root_dir (str): 根目錄的路徑。
    """
    file_name = []
    # 遍歷根目錄下的所有資料夾
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.basename(folder_name)
        # print (folder_path)
        file_name = np.append (file_name, folder_path)
        
        if os.path.isdir(folder_path):
            # 在每個資料夾中遍歷所有JSON檔案
            for json_file in os.listdir(folder_path):
                if json_file.endswith('.json'):
                    json_file_path = os.path.join(folder_path, json_file)
                    patients = np.appened ( patients, OnePatient(json_file_path), axis=0 )

    return patients, file_name

# class DataGenerator(tf.keras.utils.Sequence):
#     def __init__(self, video_paths, labels, batch_size, preprocess_fn):
#         self.video_paths = video_paths
#         self.labels = labels
#         self.batch_size = batch_size
#         self.preprocess_fn = preprocess_fn

#         self.data_augmenter = ImageDataGenerator(
#             rotation_range=20, horizontal_flip=True)
#         # self.data_augmenter = ImageDataGenerator(
#         #    rotation_range=20,
#         #    width_shift_range=0.1,
#         #    height_shift_range=0.1,
#         #    zoom_range=0.2,
#         #    horizontal_flip=True,
#         #    brightness_range=(0.8, 1.2)
#         # )

#     def __len__(self):
#         return len(self.video_paths) // self.batch_size

#     def __getitem__(self, index):
#         batch_video_paths = self.video_paths[index *
#                                              self.batch_size: (index+1)*self.batch_size]
#         batch_labels = self.labels[index *
#                                    self.batch_size: (index+1)*self.batch_size]

#         batch_video_sequences = []
#         for video_path in batch_video_paths:
#             print(video_path)
#             count = 0
#             capture = cv2.VideoCapture(video_path)
#             frames = []

#             seed = np.random.randint(0, 10000)

#             while capture.isOpened():
#                 count += 1
#                 ret, frame = capture.read()
#                 if not ret or count >= 600:
#                     break

#                 # 對每個影格進行預處理
#                 # augmented_frame = self.data_augmenter.random_transform(
#                 #    frame.astype(np.float32), seed=seed)
#                 #processed_frame = self.preprocess_fn(augmented_frame)
#                 processed_frame = self.preprocess_fn(frame)
#                 frames.append(processed_frame)
#                 #print("count : ", count)

#             capture.release()

#             batch_video_sequences.append(frames)
#             print("index : ", index)
#         return np.array(batch_video_sequences), np.array(batch_labels)


if __name__ == "__main__":
    # 指定 Excel 檔案的路徑
    path = "/media/dsp520/Grasp_2T/parkinson/GT.csv"

    # 讀取 Excel 檔案
    csv = pd.read_csv (path)

    path_json = "/media/dsp520/Grasp_2T/parkinson/LA/"
    patients = np.zeros( (42, 700, 25, 3) )
    patients, GT = process_json_files (path_json, patients)
    print( patients.shape )
    print( patients[2, 15, :] )
    print( csv.iloc[2, 0] )
    level = []
    for i in range(GT.shape[0]):
         for j in range(csv.shape[0]):
             if compare_strings( GT[i], csv.iloc[j, 0] ):
                 level = np.append (level, csv.iloc[j, 1])
                 break
    


