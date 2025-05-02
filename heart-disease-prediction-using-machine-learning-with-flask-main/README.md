# Heart Disease Prediction using Machine Learning and Flask 🫀🤖

This project is a web application built with **Flask** and **Machine Learning** that predicts the likelihood of heart disease based on user input such as age, gender, blood pressure, cholesterol level, and more.

## 🚀 Features

- Predicts the presence of heart disease using a trained ML model
- Interactive web interface using Flask
- Preprocessed dataset for higher accuracy
- User input form with real-time result display
- Easy-to-use and responsive design

## 🧠 Machine Learning

- **Algorithm used:** Logistic Regression (can be replaced with Random Forest, SVM, etc.)
- **Dataset:** [UCI Heart Disease Dataset](https://archive.ics.uci.edu/ml/datasets/Heart+Disease)
- **Libraries:** `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `flask`

## 📁 Project Structure

heart-disease-prediction-ml-flask/
│
├── static/ # CSS/JS files
├── templates/ # HTML templates
│ └── index.html
├── model/ # Trained ML model (.pkl)
├── app.py # Main Flask application
├── model_training.ipynb # Jupyter Notebook for model building
├── requirements.txt # Python dependencies
└── README.md # Project documentation

bash
Copy
Edit

## 🛠️ How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/heart-disease-prediction-ml-flask.git
   cd heart-disease-prediction-ml-flask
Install the dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the Flask app

bash
Copy
Edit
python app.py
Visit in your browser

cpp
Copy
Edit
http://127.0.0.1:5000/
📊 Sample Input Parameters
Age

Sex

Chest Pain Type

Resting Blood Pressure

Cholesterol

Fasting Blood Sugar

Rest ECG

Max Heart Rate Achieved

Exercise Induced Angina

Oldpeak

Slope

Number of Major Vessels

Thal

📷 Screenshots
![Screenshot 2025-03-09 095520](https://github.com/user-attachments/assets/001eb6c1-c327-4a99-b435-f71cc91e7875)
![Screenshot 2025-03-09 101237](https://github.com/user-attachments/assets/8a86ee76-53ea-482a-b9c3-a621897671b7)
![Screenshot 2025-03-09 101431](https://github.com/user-attachments/assets/34c15b74-03ed-489b-be15-3c2b0af6608f)
![Screenshot 2025-03-09 102016](https://github.com/user-attachments/assets/77b0281d-0afb-450a-b018-c5f7a2dd7b62)
![Screenshot 2025-03-09 102301](https://github.com/user-attachments/assets/9be15df6-a22b-4669-a3c9-ead6a19e32ae)
