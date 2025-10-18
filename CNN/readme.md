# CNN Rose Leaf Disease Detection

A Convolutional Neural Network (CNN) based project to detect diseases in rose leaves. The project includes training, prediction, and an easy setup to download the dataset from Kaggle.

---

## Table of Contents
- [Overview](#overview)
- [References](#references)
- [Dataset](#dataset)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)

---

## Overview

This project uses a CNN model to classify rose leaf images into healthy or diseased categories. The model is trained on a publicly available dataset and can predict diseases on new leaf images.  

- **Train the CNN model** on the dataset.  
- **Predict leaf disease** using the trained model.  
- **Automatic dataset download** via Kaggle API to keep the repository lightweight.  

---

## References

- **Source Code:** [GitHub Repository](https://github.com/shuvobasak4004/Rose_Leaf_Disease_Dataset)  
- **Research Paper:** [Read Paper](https://doi.org/10.5281/zenodo.8111573)  
- **Dataset:** [Kaggle Dataset](https://doi.org/10.34740/KAGGLE/DSV/6073860)  

---

## Dataset

The dataset contains images of rose leaves categorized into healthy leaves and various disease types.  

- **Automatic download:** The dataset can be downloaded directly using `download_dataset.py`.  
- **Directory after download:** `dataset/`  

> **Note:** The dataset is not included in this repository due to GitHub storage limits.  

---

## Setup

1. **Clone the repository:**
```bash
git clone <your-repo-link>
cd CNN_Model
