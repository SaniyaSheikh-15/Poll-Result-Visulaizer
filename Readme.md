# 📊 Poll Results Visualizer

A clean and interactive Streamlit-based Poll Results Visualizer that analyzes survey responses with dynamic filters, visual insights, word clouds, and export-ready CSV outputs. Includes data generator, preprocessing pipeline, and EDA utilities. Perfect for survey analytics, dashboards, and data science workflows.


# 🧠 Tech Stack

Python 3.10+
Streamlit
Pandas / NumPy
Plotly Express
Matplotlib / Seaborn
WordCloud
NLTK


# 🚀 Features

### **✔️ Upload & Process Survey Data**
- Accepts CSV exports from Google Forms or Excel  
- Automatically cleans, standardizes, and enhances data  
- Adds new features like *feedback length*  

### **✔️ Dynamic Filters**
Filter responses by:
- Preferred Tool (Python, R, Excel, Tableau, etc.)
- Gender  
- Satisfaction score range (1–5)

All charts auto-update based on filters.

### **✔️ Visualizations Included**
| Visualization | Details |
|--------------|---------|
| **Bar chart** | Popular tools chosen by respondents |
| **Histogram** | Satisfaction distribution |
| **Word Cloud** | Frequent feedback keywords |
| **Time Series** | Daily submission trends |

### **✔️ Synthetic Data Generator**
Generates realistic survey-style datasets:
- Randomized timestamps  
- Demographics  
- Tools  
- Satisfaction scores  
- Auto-generated feedback text  

Useful for testing dashboards without real data.


# ▶️ How to run

1️⃣ Create a virtual environment**
python -m venv .venv

2️⃣ Activate it
Windows:
.venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Generate sample data (optional)
python src/data_generator.py
python src/preprocess.py

5️⃣ Run the Streamlit dashboard
streamlit run app_streamlit.py


# 🤝 Contribution


Feel free to open issues or submit pull requests for enhancements or new visual components.

