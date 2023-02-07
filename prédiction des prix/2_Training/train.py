import argparse
import pandas as pd
import time
import mlflow
from mlflow.models.signature import ModelSignature
from mlflow.types.schema import Schema, ColSpec
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import  OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score
from feature_engine.encoding import RareLabelEncoder

input_schema = Schema([
  ColSpec("string", "model_key"),
  ColSpec("long", "mileage"),
  ColSpec("long", "engine_power"),
  ColSpec("string", "fuel"),
  ColSpec("string", "paint_color"),
  ColSpec("string", "car_type"),
  ColSpec("boolean", "private_parking_available"),
  ColSpec("boolean", "has_gps"),
  ColSpec("boolean", "has_air_conditioning"),
  ColSpec("boolean", "automatic_car"),
  ColSpec("boolean", "has_getaround_connect"),
  ColSpec("boolean", "has_speed_regulator"),
  ColSpec("boolean", "winter_tires")
])
output_schema = Schema([ColSpec("long")])
signature = ModelSignature(inputs=input_schema, outputs=output_schema)

if __name__ == "__main__":

    ### MLFLOW Experiment setup
    experiment_name="pricing-optimization"
    mlflow.set_experiment(experiment_name)
    experiment = mlflow.get_experiment_by_name(experiment_name)

    client = mlflow.tracking.MlflowClient()
    run = client.create_run(experiment.experiment_id)

    print("training model...")
    
    # Time execution
    start_time = time.time()

    # Call mlflow autolog
    mlflow.sklearn.autolog(log_models=False) # We won't log models right away

    # Parse arguments given in shell script
    parser = argparse.ArgumentParser()
    parser.add_argument("--min_samples_split")
    parser.add_argument("--min_samples_leaf")
    
    args = parser.parse_args()

    # Import dataset
    data = pd.read_csv('data/get_around_pricing_project.csv', index_col=0)

    # X, y split 
    X = data.loc[:,data.columns != 'rental_price_per_day']
    y = data.loc[:,data.columns == 'rental_price_per_day']

    # Rare encoding
    rare_encoder = RareLabelEncoder(tol=0.01, n_categories=5, variables=['paint_color', 'model_key'],replace_with='Other')
    X = rare_encoder.fit_transform(X)

    # Train / test split 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    # Preprocessing 
    categorical_indices = [0,3,4,5,6,7,8,9,10,11,12]
    numeric_indices=[1,2]

    ## Prepare transformers
    # Normalization
    numeric_transformer = StandardScaler()

    # OHE / dummyfication
    categorical_transformer = OneHotEncoder(drop='first', sparse=False)

    ## Combine the transformers into a single object
    featureencoder = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_indices),
            ('num', numeric_transformer, numeric_indices)
            ]
        )

    min_samples_split = int(args.min_samples_split)
    min_samples_leaf = int(args.min_samples_leaf)
    model = Pipeline(steps=[
        ("Preprocessing", featureencoder),
        ("Regressor",RandomForestRegressor(min_samples_split=min_samples_split,min_samples_leaf=min_samples_leaf ))
    ])

    # Log experiment to MLFlow
    with mlflow.start_run(run_id = run.info.run_id) as run:
        model.fit(X_train, y_train)
        y_train_pred = model.predict(X_train)

        # Log Metric 
        mlflow.log_metric("R2_train", r2_score(y_train, y_train_pred))

        # Log Param
        mlflow.log_param("min_samples_split", min_samples_split)
        mlflow.log_param("min_samples_leaf", min_samples_leaf)

        # Log model seperately to have more flexibility on setup 
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="pricing-optimization",
            registered_model_name="pricing-optimization_RF",
            signature=signature
        )
        
    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")
