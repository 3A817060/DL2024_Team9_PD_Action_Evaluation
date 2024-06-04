## Goals  
Utilize patient image data to predict the severity level of Parkinson's Disease.   

## Description   
This project aims to address the problem of quantifying the behavior of Parkinson's Disease patients through a series of tests and observations to assess the severity of Parkinson's Disease. The main action in the experiment is **Leg Agility**, which quantifies the movement of the thigh stepping by utilizing existing Deep Learning models for training and evaluation. The model optimizes its weights by learning the temporal and spatial features of the human skeleton.

## How to run   
### Install Dependencies   
```bash
# clone project   
git clone https://github.com/3A817060/DL2024_Team9_PD_Action_Evaluation.git

# install project
cd DL2024_Team9_PD_Action_Evaluation
pip install -r requirements.txt
 ```
### Data Preparation   
In this step, we need to prepare the data for further processing and analysis.
```
We will organize our data using the following structure:

- [./dataset/GT_Level.xlxs]: the PD patient's Leg Agility Ground Truth data.
- [./dataset/LA]: Location for the skeleton coordinates of each video.
 ```   
 ### Training PD_STGCN
 To train a new model or reproduce experiment results, run 
 ```python
python processor1.py
```
The training results, including model weights, configurations and loggiing files, will be saved under the `./work_dir` by default.
You can modify the training parameters such as `work_dir`, `batch_size`, `step`, `base_lr` and `device` in the configuration files. The order of priority is: `"./config/cfg.yaml"`.

## Dataset Description

This project utilizes a proprietary dataset, access to which is not publicly available. For inquiries regarding dataset access, please contact Professor **熊博安(Pao-Ann Hsiung)** whose google email is **[pahsiung@ccu.edu.tw]** for further information.

### Video Introduction:
The dataset comprises a total of 65 videos depicting individuals performing repetitive foot movements while seated in a chair. The estimated age range of the individuals is from 20 to 70 years old. Each video has a duration ranging from 32 to 38 seconds, with a frame rate of 30 frames per second.

### Body Skeleton Data:
The dataset includes a total of 44 complete skeleton joint coordinates extracted from all videos. These coordinates consist of the standard OpenPose 25 joints along with additional joints for the fingers and palms.Notably, joints related to the fingers and palms will not be utilized in this project.

## Demo

## Two stream ST_GCN

This project code is based on the work of [yysijie](https://github.com/yysijie). You can find the original repository [here](https://github.com/yysijie/st-gcn).
This project framework is based on [littlepure2333](https://github.com/littlepure2333). You can also find the original repository [here](https://github.com/littlepure2333/2s_st-gcn.git).

