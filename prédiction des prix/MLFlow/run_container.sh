   docker run -it\
    -p 4000:4000\
    -v "$(pwd):/home/app"\
    -e PORT=4000\
    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID\
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\
    -e BACKEND_STORE_URI="YOUR_BACKEND_STORE_URI"\
    -e ARTIFACT_ROOT=$ARTIFACT_ROOT\
    --platform linux/amd64\
    mrnrbn/image_bloc5_pricing python train.py