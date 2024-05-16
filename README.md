## Goals  
Utilize patient image data to predict the severity level of Parkinson's Disease.   

## Description   
This project aims to address the problem of quantifying the behavior of Parkinson's Disease patients through a series of tests and observations to assess the severity of Parkinson's Disease. The main action in the experiment is **Leg Agility**, which quantifies the movement of the thigh stepping by utilizing existing Deep Learning models for training and evaluation. The model optimizes its weights by learning the temporal and spatial features of the human skeleton.

## How to run   
### First, install dependencies   
```bash
# clone project   
git clone https://github.com/3A817060/DL2024_Team9_PD_Action_Evaluation.git

# install project
cd DL2024_Team9_PD_Action_Evaluation
pip install -r requirements.txt
 ```
### Secondly, Data Preparation   
In this step, we need to prepare the data for further processing and analysis.
```
We will organize our data using the following structure:

- [./dataset/PD_GT]: Location to store the severity Ground Truth data.
- [./dataset/Skeleton]: Location for the skeleton coordinates of each video.
- [./Video]: Location for all the videos.
 ```   
 ### Finally, training   
 To train a new model or reproduce experiment results, run 
 ```python
python main.py recognition -c config/st_gcn.twostream/train.yaml [--work_dir <work folder>]
```
The training results, including model weights, configurations and loggiing files, will be saved under the `""./work_dir""` by default or `""<work folder>""` if you appoint it.
You can modify the training parameters such as `""work_dir""`, `""batch_size""`, `""step""`, `""base_lr""` and `""device""` in the command line or configuration files. The order of priority is: command line > config file > default parameter.

## Dataset Description

This project utilizes a proprietary dataset, access to which is not publicly available. For inquiries regarding dataset access, please contact Professor **熊博安(Pao-Ann Hsiung)** whose google email is **[pahsiung@ccu.edu.tw]** for further information.

### Video Introduction:
The dataset comprises a total of 65 videos depicting individuals performing repetitive foot movements while seated in a chair. The estimated age range of the individuals is from 20 to 70 years old. Each video has a duration ranging from 32 to 38 seconds, with a frame rate of 30 frames per second.

### Body Skeleton Data:
The dataset includes a total of 44 complete skeleton joint coordinates extracted from all videos. These coordinates consist of the standard OpenPose 25 joints along with additional joints for the fingers and palms. However, for the purposes of this project, which focuses on analyzing agility through skeleton analysis, the skeleton joints (1 to 25) are decomposed to retain only the lower limb positions, specifically joints 8 to 14. These retained joints consist of 7 key points (x, y, c), representing the x and y coordinates along with detection confidence. Notably, joints related to the fingers and palms will not be utilized in this project.

## Demo

## Two stream ST_GCN

This project is based on the work of [littlepure2333](https://github.com/littlepure2333). You can find the original repository [here](https://github.com/littlepure2333/2s_st-gcn.git).

