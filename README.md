📌 Overview

This project is a data analytics dashboard built using Python, Pandas, Plotly, and Streamlit to analyze procurement data across Niagara Region Long-Term Care (LTC) homes.

The solution transforms raw procurement transaction data into actionable insights that support:

Cost optimization
Supplier performance evaluation
Procurement risk detection
Data-driven decision-making
🎯 Project Objective

The goal of this project is to identify inefficiencies in procurement operations and provide management with a decision-support tool that highlights:

High-cost suppliers
Price inconsistencies
Spending concentration
Opportunities for cost savings
🔥 Key Features
📈 Procurement Analytics
Total procurement spend across LTC homes
Cost comparison across facilities
Category-level spend analysis
🧾 Supplier Benchmarking
Compare supplier pricing against market benchmarks
Identify suppliers charging above average
⚠️ Anomaly Detection
Detect products priced significantly above average
Identify supplier concentration risks
Flag zero-cost or inconsistent data
💰 Procurement Optimization
Estimate potential savings from supplier negotiations
Highlight high-impact cost reduction opportunities
🤖 AI-Driven Insights
Automated insights for procurement improvement
Decision-support recommendations
🛠️ Tech Stack
Python
Pandas (data processing)
Plotly (visualization)
Streamlit (interactive dashboard)
ReportLab (report generation)
📂 Project Structure
niagara.region.project/
│
├── assets/                # Logo and static files
├── screenshots/           # Dashboard preview images
├── data/                  # Raw datasets (CSV)
├── pages/                 # Streamlit multi-page modules
│   ├── 1_Home_Performance.py
│   ├── 2_Procurement_Risk.py
│   ├── 3_Procurement_Optimization.py
│   ├── ...
│
├── src/                   # Core analytics logic
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── analytics_engine.py
│   ├── ai_models.py
│   ├── chat_engine.py
│
├── dashboard.py           # Main Streamlit app
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
