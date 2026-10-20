
from pathlib import Path
import joblib

models_dir = Path("models")

model_files = [
    "linear_regression.joblib",
    "ridge_regression.joblib",
    "lasso_regression.joblib",
    "elasticnet_regression.joblib",
    "decision_tree.joblib",
    "gradient_boosting.joblib",
    "knn_regressor.joblib",
    "svr.joblib",
    "polynomial_regression.joblib",
    "decision_tree_classifier.joblib",
    "gradient_boosting_classifier.joblib",
]

for filename in model_files:
    path = models_dir / filename

    if not path.exists():
        print(f"{filename}: FILE NOT FOUND")
        continue

    try:
        model = joblib.load(path)
        print(
            f"{filename}: "
            f"class={type(model).__name__}, "
            f"features={getattr(model, 'n_features_in_', 'unknown')}"
        )
    except Exception as exc:
        print(f"{filename}: LOAD ERROR: {exc}")
