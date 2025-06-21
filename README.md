# 🛡️ Fake Job Post Detection System

A modern, AI-powered tool that helps job seekers identify **fraudulent job postings** using natural language processing, machine learning, and rule-based risk analysis.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Model-Logistic%20Regression-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Working-success?style=for-the-badge" />
</p>

---

## 🚀 Features

- 🔍 **Real-time detection** of fake job listings
- 🧠 **ML model (Logistic Regression)** trained on merged real + fake datasets
- ✍️ **TF-IDF vectorizer** for intelligent text representation
- ⚠️ **Risk scoring** system for red flag phrases like “₹2000,” “no interview,” “Telegram”
- 🌐 Analyze via **direct text** or **URL scraping**
- 📊 **Confidence score**, **risk level**, and **job text insights**
- 🎨 Fully styled **Streamlit interface** with Plotly visuals

---

## 🧠 Tech Stack

| Layer          | Tools Used                                          |
|----------------|-----------------------------------------------------|
| Language       | Python 3.x                                          |
| ML Model       | Logistic Regression + TF-IDF                        |
| Frontend       | Streamlit                                           |
| NLP & Utils    | NLTK, scikit-learn, BeautifulSoup, SciPy            |
| Visualization  | Plotly                                              |

---

## 🗂️ Project Structure

├── main.py # Streamlit web app
├── Fake_job.ipynb # Model training notebook
├── lrmodel.pkl # Trained Logistic Regression model
├── vectorizer.pkl # TF-IDF vectorizer
├── requirements.txt # Python dependencies
├── data/
│ ├── fake_postings.csv # Raw fake jobs dataset
│ ├── original_fake_jobs.csv # Mixed jobs dataset
│ └── merged_fake_job_postings.csv # Cleaned, merged dataset for training
└── README.md

---

## 📦 Setup Instructions

### 🔧 Local Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/fake-job-detector.git
cd fake-job-detector

2.Install dependencies:
pip install -r requirements.txt

3.Run the app:
streamlit run main.py

🌐 Deploy to Streamlit Cloud (Optional)
Push this repo to GitHub

1.Go to streamlit.io/cloud

2.Click "New app" and select:

3.Main file: main.py

4.Branch: main

Done ✅

📊 Sample Results
| Job Example                            | Prediction   | Confidence |
| -------------------------------------- | ------------ | ---------- |
| “Earn ₹5000/day, no experience needed” | ❌ Fake       | 96.3%      |
| “Frontend Developer at Cibirix Inc.”   | ✅ Legitimate | 93.2%      |
| “Apply via Telegram for airport jobs”  | ❌ Fake       | 98.1%      |

🔐 Disclaimer
This tool is for educational and awareness purposes. It does not guarantee 100% accuracy. Always verify job postings from trusted sources and report suspected scams to relevant authorities.

👨‍💻 Author
Made with ❤️ by [Your Name]
📫 Contact: neerajchandel9.nc@gmail.com
