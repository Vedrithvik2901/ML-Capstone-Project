# Capstone Project
## Machine Learning Algorithms Review 1

Implementation of the Machine Learning Capstone Project for the course **23CSE301_ML_26_27**.

The project explores and compares multiple algorithms across three core machine learning problem types, using a real-world dataset for each:

- **Regression** — Melbourne Housing dataset
- **Classification** — Bank Marketing dataset
- **Clustering** — Online Retail dataset

Each task is organised into its corresponding dataset, notebook, saved model artifacts, and an interactive page. The goal is not simply to crown one algorithm king of the spreadsheet castle, but to understand how different algorithms behave across different datasets and problem types.

In addition to the notebooks, the repository includes an interactive **Streamlit application** (`app.py` and `pages/`) for exploring each dataset, comparing saved models, and generating predictions or customer segments.

---

## 1. Repository Structure

```text
ML-Capstone-Project/
│
├── app.py                      # Streamlit landing page
├── check_reg_models.py         # Sanity check: loads saved models and prints class / feature count
├── requirements.txt
├── README.md
│
├── pages/                      # Streamlit pages (one per ML track)
│   ├── Regression.py
│   ├── Classification.py
│   └── Clustering.py
│
├── models/                     # 26 saved .joblib artifacts (see Section 5.2)
│
├── utils/
│   └── __init__.py
│
├── data/
│   ├── classification/
│   │   ├── bank-full.csv
│   │   └── bank.csv
│   │
│   ├── clustering/
│   │   └── Online Retail.xlsx
│   │
│   └── regression/
│       └── Melbourne_housing.csv
│
└── notebooks/
    ├── classification.ipynb
    └── regression.ipynb
```

The repository separates datasets, notebooks, and saved models by machine learning task, which keeps implementations and supporting files easy to reproduce and navigate:

```text
Regression
    ├── Melbourne Housing
    ├── notebooks/regression.ipynb
    └── pages/Regression.py

Classification
    ├── Bank Marketing
    ├── notebooks/classification.ipynb
    └── pages/Classification.py

Clustering
    ├── Online Retail
    ├── data/clustering/Online Retail.xlsx
    └── pages/Clustering.py
```

---

## 2. Regression

### 2.1 Dataset

The regression task uses the **Melbourne Housing** dataset, which contains information about properties sold in Melbourne.

The original dataset contains **34,857 records and 22 columns**, including:

- Number of rooms
- Property type
- Distance from the city
- Land size
- Building area
- Year built
- Location information
- Property selling method
- Region
- Property count
- Sale price

Target variable:

```text
Price
```

Dataset location:

```text
data/regression/Melbourne_housing.csv
```

### 2.2 Problem Statement

Develop machine learning models capable of predicting Melbourne property prices from available property and location characteristics.

The workflow includes exploratory data analysis, data cleaning, feature engineering, preprocessing, model training, hyperparameter tuning, cross-validation, and final model evaluation.

### 2.3 Exploratory Data Analysis

The regression notebook includes:

- Feature distribution analysis
- Missing-value analysis
- Target distribution
- Correlation heatmap
- Feature-target scatter plots
- Categorical feature analysis
- Outlier investigation

The EDA was used to understand the structure of the dataset and guide subsequent preprocessing and feature-engineering decisions.

### 2.4 Data Preprocessing

1. Rows with missing target (`Price`) values were removed.
2. `BuildingArea` was converted to a numerical representation, with invalid values treated as missing.
3. The `Date` column was converted to a datetime representation.
4. Invalid `YearBuilt` values were treated as missing.
5. Infinite values were converted to missing values.
6. Duplicate records were checked.
7. A domain-based feature, `PropertyAge`, was created:

```text
PropertyAge = SaleYear - YearBuilt
```

`PropertyAge` represents the age of a property at the time of sale and may capture effects related to depreciation, maintenance, and buyer preferences.

8. Numerical features were processed using median imputation followed by standard scaling.
9. Categorical features were processed using most-frequent imputation followed by one-hot encoding.
10. Preprocessing transformations were fitted only on the training data and then applied to the test data.

An **80:20 train-test split** with `random_state=42` was used. The same held-out test set was used for all regression models.

Extreme but plausible property observations were retained rather than automatically removed using the IQR rule. Clearly invalid observations were handled separately during data cleaning.

### 2.5 Regression Algorithms

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

The models were evaluated using **R²**, **RMSE**, and **MAE**.

### 2.6 Regression Model Comparison

All models were evaluated on the same held-out test set.

| Rank | Model | R² | RMSE | MAE |
|---:|---|---:|---:|---:|
| 1 | Random Forest Regressor | 0.7958 | 281,394.33 | 164,873.02 |
| 2 | Gradient Boosting Regressor | 0.7824 | 290,526.34 | 181,163.82 |
| 3 | Support Vector Regressor (SVR) | 0.7441 | 315,039.09 | 202,327.20 |
| 4 | K-Nearest Neighbors Regressor | 0.7340 | 321,189.63 | 199,670.59 |
| 5 | Polynomial Regression | 0.7063 | 337,490.29 | 218,440.21 |
| 6 | Ridge Regression | 0.6866 | 348,641.65 | 230,611.83 |
| 7 | Lasso Regression | 0.6855 | 349,274.87 | 230,636.29 |
| 8 | Linear Regression | 0.6831 | 350,550.70 | 231,653.14 |
| 9 | Decision Tree Regressor | 0.6484 | 369,264.82 | 220,509.08 |
| 10 | ElasticNet Regression | 0.2309 | 546,159.13 | 384,473.93 |

### 2.7 Hyperparameter Tuning

`GridSearchCV` was used for hyperparameter tuning.

**Gradient Boosting**

| Metric | Baseline | Tuned |
|---|---:|---:|
| R² | 0.7657 | 0.7824 |
| RMSE | 301,427.30 | 290,526.34 |
| MAE | 188,323.53 | 181,163.82 |

Selected learning rate:

```text
learning_rate = 0.2
```

**Support Vector Regression**

The SVR was tuned over different values of `C` and kernel types.

```text
C = 10
kernel = rbf
```

The tuned model was evaluated on the held-out test set after inverse-transforming the scaled target.

**K-Nearest Neighbors**

The KNN model was tuned over different values of `n_neighbors`.

```text
k = 11
```

| Metric | Baseline | Tuned |
|---|---:|---:|
| R² | 0.7068 | 0.7340 |
| RMSE | 337,217.90 | 321,189.63 |
| MAE | 207,136.25 | 199,670.59 |

### 2.8 Cross-Validation

Five-fold cross-validation was performed for the two strongest regression models.

| Model | Mean R² | Standard Deviation |
|---|---:|---:|
| Random Forest Regressor | 0.7679 | 0.0158 |
| Gradient Boosting Regressor | 0.7428 | 0.0135 |

### 2.9 Regression Model Interpretation

The regression notebook includes an actual vs. predicted plot, a residual plot, and a Random Forest feature-importance plot.

Important Random Forest features include variables related to:

- Region
- Number of rooms
- Distance from the city
- Land size
- Property type
- Building area
- Geographic location

Feature importance is interpreted as a model-specific measure and does not imply a causal relationship.

### 2.10 Interactive Regression Page

`pages/Regression.py` provides three tabs:

- **Overview** — dataset file name, row count, and summary information.
- **Explore data** — interactive exploration of the Melbourne Housing data.
- **Predict a price** — a form for entering property details and estimating a sale price with a selected saved model.

The prediction form collects rooms, bedrooms, bathrooms, car spaces, distance from the city, land size, building area, year built, sale year, latitude and longitude, property count, suburb, region, postcode, council area, property type, selling method, seller, and parking area. `PropertyAge` is computed from the sale year and year built, and the input is rejected if the sale year precedes the year built.

Inputs are transformed with the saved `housing_preprocessor.joblib`, so the page applies the same preprocessing as the notebook. Model-specific handling is included where the training workflow required it:

- **Polynomial Regression** — numerical features are expanded using the saved `polynomial_artifacts.joblib` before being recombined with the remaining encoded features.
- **Support Vector Regression** — because the SVR was trained on a scaled target, predictions are passed through `svr_target_scaler.joblib` to return prices in Australian dollars.

The predicted price is a model estimate, not a property valuation.

Models available in the prediction form:

Linear Regression, Ridge Regression, Lasso Regression, Elastic Net, Decision Tree, Gradient Boosting, K-Nearest Neighbors, Support Vector Regression, and Polynomial Regression.

> Random Forest, the best-performing model in Section 2.6, is not currently selectable in the prediction form.

---

## 3. Classification

### 3.1 Dataset

The classification task uses the **Bank Marketing** dataset, which contains demographic, financial, and campaign-related attributes for clients contacted during a bank marketing campaign.

```text
data/classification/bank.csv        # initial experimentation
data/classification/bank-full.csv   # final classification analysis and Streamlit page
```

The files are semicolon-separated.

Target variable (`y`):

- `yes` — Customer subscribed to a term deposit
- `no` — Customer did not subscribe

### 3.2 Problem Statement

Develop machine learning models that predict whether a customer will subscribe to the bank's term deposit based on the available customer and campaign information. Final model evaluation is performed on an unseen test set.

### 3.3 Classification Workflow

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

Preprocessing summary:

- A feature, `previously_contacted`, is derived from `pdays` (`1` when `pdays` is not `-1`, otherwise `0`).
- Numerical features are standardised with `StandardScaler`.
- Categorical features are encoded with `OneHotEncoder(handle_unknown="ignore")`.
- A stratified **80:20 train-test split** with `random_state=42` is used, so the class balance is preserved in both splits.

### 3.4 Classification Algorithms

| # | Algorithm | Notes |
|---|-----------|-------|
| 1 | Logistic Regression | Baseline classifier; interpret coefficients and odds |
| 2 | K-Nearest Neighbors | Tune `k`; examine distance metrics |
| 3 | Gaussian Naive Bayes | Examine the conditional independence assumption |
| 4 | Decision Tree Classifier | Tune `max_depth`; visualise the tree |
| 5 | Support Vector Machine (SVC) | Tune `C` and kernel; scale features |
| 6 | Random Forest | Bagged ensemble of decision trees |
| 7 | AdaBoost | Sequential boosting of weak learners |
| 8 | Gradient Boosting | Boosted tree ensemble |
| 9 | Bagging Classifier | Bootstrap aggregation of base classifiers |
| 10 | Multi-Layer Perceptron (MLP) | Feed-forward neural network |

Algorithms 1–5 form the required Part A set. Algorithms 6–10 are additional saved models that are also available in the interactive Streamlit page.

Detailed model outputs and visualizations are available in `notebooks/classification.ipynb`.

### 3.5 Evaluation Metrics

Because the Bank Marketing dataset contains an imbalanced target variable, accuracy alone does not provide a complete picture of model performance.

- **Accuracy** — Overall proportion of correct predictions
- **Precision** — Proportion of predicted subscribers who actually subscribed
- **Recall** — Proportion of actual subscribers correctly identified
- **F1 Score** — Balance between precision and recall
- **Confusion Matrix** — Detailed breakdown of correct and incorrect predictions

Particular attention is given to the positive class, `yes`, because it represents the minority subscription class.

### 3.6 Key Classification Insights

The dataset contains substantially more customers who did not subscribe to a term deposit than customers who did. This creates several important modelling considerations:

- High accuracy does not necessarily mean that a model identifies subscribers effectively.
- Recall and F1 score are important for evaluating performance on the minority class.
- Hyperparameter tuning can change the balance between precision, recall, and overall accuracy.
- Different algorithms may be preferable depending on whether the priority is reducing false positives or identifying more potential subscribers.
- The `duration` feature (last contact duration in seconds) is only known after a call has taken place, so predictions that rely on it are not realistic for deciding whom to call in advance.

The project therefore compares models using multiple evaluation metrics rather than selecting a model based solely on accuracy.

### 3.7 Interactive Classification Page

`pages/Classification.py` ("Classification Studio") provides four tabs:

- **Overview** — dataset description, target distribution, feature types, a dataset preview, and summary statistics.
- **Explore Data** — individual feature distributions and feature-versus-subscription comparisons.
- **Evaluate Models** — select any of the ten saved classifiers and evaluate them on the stratified 20% test split, with accuracy, precision, recall, and F1 for the `yes` class, plus a confusion matrix and classification report.
- **Predict** — enter a customer's details and obtain the selected model's subscription prediction.

The page rebuilds the notebook's preprocessing pipeline (scaling and one-hot encoding) from the dataset, so the saved models receive the same feature representation used during training.

---

## 4. Clustering

### 4.1 Dataset

The clustering task uses the **Online Retail** dataset, which contains transactional information from an online retail business, including products, quantities, prices, customers, and transaction dates.

```text
data/clustering/Online Retail.xlsx
```

Because clustering is an unsupervised learning task, no target variable is required.

### 4.2 Problem Statement

Identify meaningful groups of customers based on their purchasing behaviour. The clustering workflow includes data preparation, feature construction, exploratory analysis, clustering, and interpretation of the resulting groups.

### 4.3 Data Preparation

Transaction records are cleaned and aggregated into customer-level features:

1. Duplicate transactions are removed.
2. Rows without a `CustomerID` are removed, since customer-level aggregation requires it.
3. Cancelled invoices (invoice numbers starting with `C`) are removed.
4. Rows with non-positive `Quantity` or `UnitPrice` are removed.
5. A `Sales` value (`Quantity × UnitPrice`) is calculated for each transaction line.
6. Transactions are aggregated per customer into four features.
7. Infinite, missing, and non-positive feature values are removed.
8. Features are transformed with `log1p` to reduce skew, then standardised with `StandardScaler`.

### 4.4 Customer Features

| Feature | Meaning |
|---|---|
| `Frequency` | Number of distinct invoices for a customer |
| `Monetary` | Total sales value associated with the customer |
| `AverageOrderValue` | Monetary value divided by invoice frequency |
| `UniqueProducts` | Number of distinct products purchased |

### 4.5 Clustering Algorithms

| # | Algorithm | Notes |
|---|-----------|-------|
| 1 | K-Means Clustering | Partitions customers into a predefined number of clusters by minimising within-cluster squared distances; the saved model can assign a new transformed customer profile |
| 2 | Agglomerative Clustering | Builds clusters hierarchically by repeatedly merging groups; has no `predict()` method, so it cannot assign unseen customers directly |

### 4.6 Clustering Evaluation

Because there are no ground-truth labels, clusterings are compared using internal validity metrics:

- **Silhouette Score** — how well each customer fits its own cluster compared with the nearest other cluster (higher is better).
- **Davies-Bouldin Index** — average similarity between each cluster and its most similar cluster (lower is better).
- **Calinski-Harabasz Score** — ratio of between-cluster to within-cluster dispersion (higher is better).

### 4.7 Interactive Clustering Page

`pages/Clustering.py` ("Customer Segmentation") provides four tabs:

- **Overview** — project description, algorithm summaries, feature definitions, and a data cleaning summary showing how many transactions and customers remain after each step.
- **Explore Data** — a customer feature sample, descriptive statistics, feature distributions, a correlation view, and the log-transformed features.
- **Cluster Analysis** — choose K-Means or Agglomerative Clustering, then view the evaluation metrics, cluster sizes, a two-dimensional PCA projection of the clusters, median feature profiles per cluster, and a browsable table of assigned customers.
- **Customer Segmentation** — select an existing `CustomerID` to see its features and assigned cluster, or enter the four feature values for a new customer profile and have K-Means assign it to a cluster.

The page reproduces the notebook's cleaning, aggregation, `log1p`, and scaling pipeline. For Agglomerative Clustering, which cannot predict on new data, the page re-fits the model with three clusters on the prepared data to obtain labels.

---

## 5. Interactive Application

### 5.1 Streamlit Application

The Streamlit app is a multi-page workspace with a dark theme.

- `app.py` is the landing page. It shows the number of datasets and saved model artifacts found in the repository, cards linking to each track, and tables listing the available datasets and `.joblib` files.
- `pages/Regression.py`, `pages/Classification.py`, and `pages/Clustering.py` are the three track pages described in Sections 2.10, 3.7, and 4.7.
- `check_reg_models.py` is a standalone script that loads selected saved models and prints their class and expected number of input features, which is useful for diagnosing artifact or version problems.

Run it from the repository root:

```bash
streamlit run app.py
```

### 5.2 Saved Model Artifacts

The `models/` directory contains 26 serialised `.joblib` files.

| Track | Artifacts |
|---|---|
| Regression | `linear_regression`, `ridge_regression`, `lasso_regression`, `elasticnet_regression`, `decision_tree_regressor`, `gradient_boosting_regressor`, `knn_regressor`, `svr`, `polynomial_regression` |
| Regression support | `housing_preprocessor` (fitted preprocessing pipeline), `polynomial_artifacts` (polynomial transformer and column indices), `svr_target_scaler` (target scaler for SVR) |
| Classification | `logistic_regression`, `knn`, `decision_tree_classifier`, `gaussian_nb`, `svm`, `random_forest`, `adaboost`, `gradient_boosting_classifier`, `bagging`, `mlp_classifier` |
| Clustering | `kmeans_clustering`, `agglomerative_clustering` |
| Other | `decision_tree`, `gradient_boosting` (referenced only by `check_reg_models.py`) |

Saved models should be loaded with the same scikit-learn version used to train them; a mismatch can cause load warnings or errors.

---

## 6. Technologies and Libraries

**Machine learning and analysis**

- Python
- Jupyter Notebook
- pandas
- NumPy
- SciPy
- Matplotlib
- Seaborn
- scikit-learn
- joblib
- openpyxl (reading the Online Retail Excel file)

**Interactive application**

- Streamlit

---

## 7. Environment Setup and How to Run

1. Clone the repository:

```bash
git clone https://github.com/Vedrithvik2901/ML-Capstone-Project.git
cd ML-Capstone-Project
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure that the datasets are present in the corresponding `data/` directories.

4. Choose how to explore the project:

**Notebooks**

Open the required notebook from `notebooks/` and run it from top to bottom.

```text
notebooks/regression.ipynb
notebooks/classification.ipynb
```

The notebooks contain the complete implementation, including data preparation, analysis, model training, evaluation, and visualizations.

**Streamlit application**

```bash
streamlit run app.py
```

---

## 8. Reproducibility

A fixed `random_state=42` is used where applicable to make experiments reproducible.

For the regression task, all models use the same 80:20 train-test split and the same held-out test set to ensure a consistent comparison. Preprocessing transformations are fitted using training data before being applied to the test data.

For the classification task, the 80:20 split is stratified on the target so that class proportions are preserved.

The Streamlit pages reconstruct the notebooks' preprocessing and splits so that the saved models are evaluated and queried consistently with the notebook results.

---

## 9. Project Goals

This repository provides hands-on practice with:

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
- Model persistence and use in an interactive Streamlit application

---

## 10. AI Assistance

Generative AI tools were used as an assistance resource during development of the project, primarily for code scaffolding, debugging support, explanation of machine learning concepts, and documentation assistance.

The analysis, model evaluation, interpretation of results, and final project decisions were reviewed and performed as part of the project workflow.

---

## 11. Git and Version History

The project was developed incrementally using Git. Meaningful commits were maintained throughout development to document major stages such as:

- Dataset integration
- Project setup
- Data cleaning
- Exploratory data analysis
- Feature engineering
- Preprocessing
- Model implementation
- Hyperparameter tuning
- Model evaluation
- Interactive application development
- Documentation

The repository therefore maintains a traceable development history rather than relying on a single final commit.

---

## 12. Project Status

- **Regression:** Complete — all ten required regression algorithms, model comparison, hyperparameter tuning, and cross-validation. Nine of the ten models are available in the interactive prediction page.
- **Classification:** The five required Part A algorithms and the full evaluation workflow are complete. Five additional models (Random Forest, AdaBoost, Gradient Boosting, Bagging, and MLP) are saved and available in the interactive page.
- **Clustering:** K-Means and Agglomerative Clustering are implemented on customer-level features, evaluated with internal validity metrics, and available in the interactive page.
- **Interactive application:** Streamlit pages for all three tracks are in place.

Known limitations:

- Classification predictions that use `duration` are not realistic for pre-call targeting.
- Predicted house prices are model estimates, not valuations.

The project will continue to be updated as additional analysis, evaluation results, and documentation are completed.
