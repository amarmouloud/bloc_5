## Training a model with MLFlow

1. Add your MLFlow server URL in the `secrets.sh` file created during the first step
``` 
export MLFLOW_TRACKING_URI='YOUR_APP_URL'
```
Then run 
```
source PATH_TO_SECRETS/secrets.sh
```
2. We will reuse the Docker image that we created during the first step. If this is not the case, place yourself in the `1_MLFlow_setup` folder and run `docker buildx build --platform linux/amd64 -t YOUR_IMAGE_NAME . `
3. Train your model `mlflow run . -P alpha=1.0`. Replace the value of `alpha`with the value you want to train your model.
