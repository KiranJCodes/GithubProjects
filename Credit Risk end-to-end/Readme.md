```markdown
# German Credit Risk Analysis - End to End Project

A comprehensive machine learning project for credit risk assessment using German credit data. This project covers the full data science pipeline from EDA to model deployment.

## 📊 Project Overview

Predict credit risk (good/bad) based on customer demographic and financial information using multiple machine learning models.

## 🚀 Features

- **Data Analysis**: Comprehensive EDA with visualizations
- **Multiple Models**: XGBoost, Random Forest, Extra Trees, Decision Tree
- **Hyperparameter Tuning**: GridSearchCV for optimal performance
- **Model Comparison**: Accuracy and ROC analysis
- **Web Interface**: Streamlit app for predictions

## 📁 Project Structure

```
Credit-Risk-end-to-end/
├── Main.py                    # Main analysis script
├── app.py                     # Streamlit web interface
├── XGB_Classifier_model.pkl   # Trained model
├── *_encoder.pkl              # Label encoders for categorical features
└── README.md
```

## 🔧 Installation

```bash
# Clone the repository
git clone "https://github.com/KiranJCodes/GithubProjects/tree/main/Credit%20Risk%20end-to-end"
cd "Credit Risk end-to-end"
```

## 📈 Model Performance

| Model         | Accuracy |
| ------------- | -------- |
| XGBoost       | 0.67     |
| Random Forest | 0.62     |
| Extra Trees   | 0.62     |
| Decision Tree | 0.6      |

## 🎯 Usage

### Run Analysis
```bash
python Main.py
```

### Launch Web App
```bash
streamlit run app.py
```

## 📋 Data Features

- **Demographic**: Age, Sex, Job
- **Financial**: Credit amount, Duration, Savings/Checking accounts
- **Loan Details**: Purpose, Housing
- **Target**: Risk (Good/Bad)

## 🔍 Key Insights

- Identified key risk factors through EDA
- Credit amount and duration strongly correlate with risk
- Certain job types and purposes show higher default rates
- XGBoost achieved highest prediction accuracy

## 🛠️ Technologies Used

- Python 3.9
- Pandas, NumPy
- Scikit-learn, XGBoost
- Matplotlib, Seaborn
- Streamlit
- Joblib

## 📊 Results

- Comprehensive model comparison with ROC curves
- Feature importance analysis
- Production-ready model export
- Interactive web interface for predictions

## 🤝 Contributing

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request
```

