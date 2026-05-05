# ⚡ AI-Based Energy Management System using AWS IoT

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![AWS](https://img.shields.io/badge/AWS-IoT-orange)
![ML](https://img.shields.io/badge/Machine%20Learning-LSTM%20%7C%20XGBoost-green)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

An intelligent **Energy Management System (EMS)** built using **AWS IoT + Machine Learning** for real-time monitoring, prediction, and anomaly detection in energy consumption.

---

## 🚀 Overview

This system combines:
- IoT data ingestion (MQTT)
- AWS cloud services
- Machine learning models

to transform energy systems from **reactive monitoring → predictive optimization**.

Based on our research work:
- IoT-based EMS :contentReference[oaicite:0]{index=0}  
- AI-Enhanced Predictive EMS :contentReference[oaicite:1]{index=1}  

---

## 🧠 Key Features

- 📡 Real-time data ingestion via AWS IoT Core
- ☁️ Serverless processing with AWS Lambda
- 🗄️ Scalable storage using DynamoDB
- 📊 Live monitoring via CloudWatch
- 🚨 Alert system using SNS
- 🤖 ML-based predictions:
  - LSTM (time-series forecasting)
  - XGBoost (error correction)
- 🧠 Hybrid anomaly detection:
  - Predictive deviation
  - Isolation Forest

---

## 🏗️ Architecture
```
IoT Device / CSV Data
↓
AWS IoT Core (MQTT)
↓
AWS Lambda
↓
DynamoDB + CloudWatch
↓
ML Models (LSTM + XGB + IF)
↓
Alerts (SNS)
```
---

## 📂 Project Structure
```
├── data/
├── models/
├── src/
│ ├── data_loader.py
│ ├── features.py
│ ├── lstm_model.py
│ ├── xgb_model.py
│ ├── isolation_forest_model.py
│ ├── hybrid_model.py
│ ├── anomaly.py
│
├── train.py
├── test.py
├── main.py
```
---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/energy-management-system.git
cd energy-management-system

pip install -r requirements.txt
```
## 🏋️ Train the Models
```bash
python train.py
```
This will:

- Train LSTM model (time-series prediction)
- Train XGBoost model (residual correction)
- Train Isolation Forest (anomaly detection)
- Save models in /models

## 🧪 Run Prediction & Anomaly Detection
```bash 
python test.py
```

### Example Output:
```
========== EMS OUTPUT ==========
Predicted : 2450.12
Actual    : 2520.45
Deviation : 70.33 (threshold 50.00)
Dev Status: ANOMALY
IF Status : NORMAL
FINAL     : ANOMALY
================================
```
## ⚙️ Core Logic
### 🔹 Hybrid Prediction

LSTM predicts base value → XGBoost corrects error:

```python
final_prediction = lstm_prediction + residual_correction
```
### 🔹 Anomaly Detection Logic
```
ANOMALY if:

|Actual - Predicted| > Adaptive Threshold
        OR
Isolation Forest detects anomaly
```
This reduces false positives compared to traditional threshold-based systems.

## 🧰 Tech Stack
- Programming: Python
- Machine Learning: TensorFlow (LSTM), XGBoost, Scikit-learn
- Cloud: AWS IoT Core, Lambda, DynamoDB, CloudWatch, SNS
- Data Processing: Pandas, NumPy


## 📊 Improvements Over Traditional Systems

| Feature       | Traditional EMS | This System     |
|--------------|----------------|----------------|
| Monitoring    | Static         | Real-time      |
| Prediction    | ❌             | ✅             |
| Alerts        | Fixed          | Adaptive + ML  |
| Intelligence  | Reactive       | Predictive     |


## 🔮 Future Scope
- Reinforcement learning for energy optimization
- Multi-device & multi-location monitoring
- Renewable energy integration
- Advanced dashboards (AWS QuickSight)


## 📄 Research Basis

This project is based on:

- IoT-based Energy Management System using AWS
- AI-Enhanced Predictive Energy Management System with ML

## 👨‍💻 Authors
- Sohail Akhtar
- Rahul Choudhary
- Anjali Gupta
- Gaurav Raj

Sharda University, Greater Noida

## ⭐ Support

If you found this project useful:

- ⭐ Star this repository
- 🔁 Share it
- 🤝 Contribute
