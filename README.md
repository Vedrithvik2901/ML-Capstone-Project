# Machine Learning Algorithms Review

A structured machine learning project that explores and compares multiple algorithms across three core machine learning problem types:

- **Regression**
- **Classification**
- **Clustering**

The project is designed as an algorithm review and comparison exercise, with datasets and models organized by problem type.

---

## Project Structure

```text
ML-Algorithms-Review/
│
├── data/
│   ├── classification/
│   │   ├── bank-full.csv
│   │   └── bank.csv
│   ├── clustering/
│   │   └── Online Retail.xlsx
│   └── regression/
│       └── Melbourne_housing.csv
│
├── notebooks/
│   ├── classification.ipynb
│   └── regression.ipynb
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

# Datasets

## Classification: Bank Marketing Dataset

The classification task uses the Bank Marketing dataset. The objective is to predict whether a customer will subscribe to a term deposit.

### Target Variable

- `yes` — Customer subscribed to a term deposit
- `no` — Customer did not subscribe

The project uses:

- `bank.csv` for initial experimentation
- `bank-full.csv` for the final classification analysis

Final model evaluation is performed on an unseen test set.

---

## Regression: Melbourne Housing Dataset

The regression task uses the Melbourne Housing dataset to explore and predict housing-related numerical values.

---

## Clustering: Online Retail Dataset

The clustering task uses the Online Retail dataset to identify meaningful groups and patterns based on customer or transaction behaviour.

Because clustering is an unsupervised learning task, no target variable is required.

---

# Algorithms

## Regression Algorithms

| # | Algorithm | Notes |
|---|-----------|-------|
| 1 | Linear Regression | Baseline model; interpret coefficients |
| 2 | Ridge Regression | L2 regularisation; tune `alpha` |
| 3 | Lasso Regression | L1 regularisation; observe feature sparsity |
| 4 | ElasticNet Regression | Combined L1 + L2 regularisation; tune `l1_ratio` |
| 5 | Polynomial Regression | Apply polynomial features and compare degrees |
| 6 | Decision Tree Regressor | Tune `max_depth`; examine feature importance |
| 7 | Random Forest Regressor | Ensemble model; tune `n_estimators` |
| 8 | Gradient Boosting Regressor | Tune learning rate and boosting parameters |
| 9 | Support Vector Regressor (SVR) | Scale features; tune `C` and kernel |
| 10 | K-Nearest Neighbors Regressor | Tune `k`; examine the impact of scaling |

## Classification Algorithms

| # | Algorithm | Notes |
|---|-----------|-------|
| 1 | Logistic Regression | Baseline classifier; interpret coefficients and odds |
| 2 | K-Nearest Neighbors | Tune `k`; examine distance metrics |
| 3 | Gaussian Naive Bayes | Examine the conditional independence assumption |
| 4 | Decision Tree Classifier | Tune `max_depth`; visualise the tree |
| 5 | Support Vector Machine (SVC) | Tune `C` and kernel; scale features |

---

# Classification Workflow

The classification analysis follows a structured machine learning workflow:

1. Load the dataset
2. Perform a dataset audit
3. Explore numerical and categorical feature distributions
4. Analyse the target class distribution
5. Identify missing values and duplicate records
6. Perform correlation analysis
7. Analyse potential outliers
8. Prepare features and the target variable
9. Split the data into training and test sets
10. Apply appropriate preprocessing
11. Train machine learning models
12. Evaluate models using the unseen test set
13. Tune selected hyperparameters
14. Compare model performance

---

# Classification Evaluation Metrics

Because the Bank Marketing dataset contains an imbalanced target variable, accuracy alone does not provide a complete picture of model performance.

The following metrics are considered:

- **Accuracy** — Overall proportion of correct predictions
- **Precision** — Proportion of predicted subscribers who actually subscribed
- **Recall** — Proportion of actual subscribers correctly identified
- **F1 Score** — Balance between precision and recall
- **Confusion Matrix** — Detailed breakdown of correct and incorrect predictions

Particular attention is given to the positive class, `yes`, because it represents the minority subscription class.

---

# Key Classification Insights

The classification dataset contains substantially more customers who did not subscribe to a term deposit than customers who did.

This creates several important modelling considerations:

- High accuracy does not necessarily mean that a model identifies subscribers effectively.
- Recall and F1 score are important for evaluating performance on the minority class.
- Hyperparameter tuning can change the balance between precision, recall, and overall accuracy.
- Different algorithms may be preferable depending on whether the priority is reducing false positives or identifying more potential subscribers.

The project therefore compares models using multiple evaluation metrics rather than selecting a model based solely on accuracy.

---

# Technologies and Libraries

The project is implemented in Python using:

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

Install the dependencies with:

```bash
pip install -r requirements.txt
```

---

# How to Run

1. Clone the repository:

```bash
git clone <repository-url>
```

2. Navigate to the project directory:

```bash
cd ML-Algorithms-Review
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Start Jupyter Notebook:

```bash
jupyter notebook
```

5. Open and run the notebooks inside the `notebooks/` directory.

---

# Project Goals

This repository is intended to provide hands-on practice with:

- Data cleaning
- Exploratory data analysis
- Feature preprocessing
- Encoding categorical variables
- Feature scaling
- Train-test splitting
- Regression modelling
- Classification modelling
- Unsupervised clustering
- Hyperparameter tuning
- Model evaluation
- Algorithm comparison

The goal is not simply to crown one algorithm king of the spreadsheet castle 👑, but to understand how different machine learning algorithms behave across different datasets and problem types.

---

## Project Status

🚧 **Work in Progress**

- Classification analysis is currently implemented.
- Additional regression models will be added.
- Clustering analysis will be added as the project develops.
