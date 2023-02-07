## Set up an API with FastAPI 

1. Build your Docker image `docker buildx build --platform linux/amd64 -t YOUR_IMAGE_NAME .`
2. Log in Heroku `heroku login`
3. Create your application `heroku create YOUR_APP_NAME`
4. Set the configuration variables needed by the app. Run `source PATH_to_SECRETS/secrets.sh`and then `source heroku_config.sh`
8. Ship your container to Heroku. Run successively:
```
docker tag YOUR_IMAGE_NAME registry.heroku.com/YOUR_APP_NAME/web
heroku container:login
docker push registry.heroku.com/YOUR_APP_NAME/web
heroku container:release web -a YOUR_APP_NAME
```
9. Check the result ! `heroku open -a YOUR_APP_NAME`

My API server can be found [here](https://bloc5-pricing-prediction.herokuapp.com/)
