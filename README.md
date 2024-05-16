### Deep learning project seed
Use this seed to start new deep learning / ML projects.

- Built in setup.py
- Built in requirements
- Examples with MNIST
- Badges
- Bibtex

#### Goals  
The goal of this seed is to structure ML paper-code the same so that work can easily be extended and replicated.   

### DELETE EVERYTHING ABOVE FOR YOUR PROJECT  
 
---

<div align="center">    
 
# Your Project Name     

[![Paper](http://img.shields.io/badge/paper-arxiv.1001.2234-B31B1B.svg)](https://www.nature.com/articles/nature14539)
[![Conference](http://img.shields.io/badge/NeurIPS-2019-4b44ce.svg)](https://papers.nips.cc/book/advances-in-neural-information-processing-systems-31-2018)
[![Conference](http://img.shields.io/badge/ICLR-2019-4b44ce.svg)](https://papers.nips.cc/book/advances-in-neural-information-processing-systems-31-2018)
[![Conference](http://img.shields.io/badge/AnyConference-year-4b44ce.svg)](https://papers.nips.cc/book/advances-in-neural-information-processing-systems-31-2018)  
<!--
ARXIV   
[![Paper](http://img.shields.io/badge/arxiv-math.co:1480.1111-B31B1B.svg)](https://www.nature.com/articles/nature14539)
-->
![CI testing](https://github.com/PyTorchLightning/deep-learning-project-template/workflows/CI%20testing/badge.svg?branch=master&event=push)


<!--  
Conference   
-->   
</div>
 
## Description   
What it does   

## How to run   
First, install dependencies   
```bash
# clone project   
git clone https://github.com/YourGithubName/deep-learning-project-template

# install project   
cd deep-learning-project-template 
pip install -e .   
pip install -r requirements.txt
 ```   
 Next, navigate to any file and run it.   
 ```bash
# module folder
cd project

# run module (example: mnist as your main contribution)   
python lit_classifier_main.py    
```

## Imports
This project is setup as a package which means you can now easily import any file into any other file like so:
```python
from project.datasets.mnist import mnist
from project.lit_classifier_main import LitClassifier
from pytorch_lightning import Trainer

# model
model = LitClassifier()

# data
train, val, test = mnist()

# train
trainer = Trainer()
trainer.fit(model, train, val)

# test using the best model!
trainer.test(test_dataloaders=test)
```
## Dataset

This project utilizes a proprietary dataset, access to which is not publicly available. For inquiries regarding dataset access, please contact Professor Pahsiung (pahsiung@ccu.edu.tw) for further information.

### Video Introduction:
The dataset comprises a total of 65 videos depicting individuals performing repetitive foot movements while seated in a chair. The estimated age range of the individuals is from 20 to 70 years old. Each video has a duration ranging from 32 to 38 seconds, with a frame rate of 30 frames per second.

### Body Skeleton Data:
The dataset includes a total of 44 complete skeleton joint coordinates extracted from all videos. These coordinates consist of the standard OpenPose 25 joints along with additional joints for the fingers and palms. However, for the purposes of this project, which focuses on analyzing agility through skeleton analysis, the skeleton joints (1 to 25) are decomposed to retain only the lower limb positions, specifically joints 8 to 14. These retained joints consist of 7 key points (x, y, c), representing the x and y coordinates along with detection confidence. Notably, joints related to the fingers and palms will not be utilized in this project.


## Two stream ST_GCN

This project is based on the work of [littlepure2333](https://github.com/littlepure2333). You can find the original repository [here](https://github.com/littlepure2333/2s_st-gcn.git).

