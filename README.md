Hi Chris,

I wanted to give you a quick rundown of deploying GPU APIs on paperspace. I think working backwards might be a reasonable way to walk through the code. To deploy this code:

    git clone https://github.com/amarder/deployolo.git
    cd deployolo
    pspace deployment up -c paperspace.json

This sets up a few things:

1.  Autogenerated API Documentation: `<endpoint>/docs`

2.  NVIDIA-SMI output: `<endpoint>/nvidia-smi/`

    Underlying code: https://github.com/amarder/deployolo/blob/main/main.py#L37-L41

3.  TensorFlow physical devices: `<endpoint>/devices/`

    Underlying code: https://github.com/amarder/deployolo/blob/main/main.py#L43-L47

4.  YOLO predictions: `<endpoint>/yolo/`

    Underlying code: https://github.com/amarder/deployolo/blob/main/main.py#L10-L35

I use numbers 2 and 3 to make sure that paperspace is using the GPU. To get a YOLO prediction I post a jpeg file to the API using the `requests` package like so:

    import requests
    with open('image.jpg', 'rb') as f:
        response = requests.post('<endpoint>/yolo/', files={'file': f})

Things to keep in mind:

1.  We're deploying a public image.
    - We tell paperspace what image to deploy here: https://github.com/amarder/deployolo/blob/main/paperspace.json#L3
    - I've posted it on Docker Hub here: https://hub.docker.com/repository/docker/amarder/yolo/general
    - I posted it with the following commands:

        ```
        git clone https://github.com/amarder/deployolo.git
        cd deployolo
        docker build . -t amarder/yolo
        docker push amarder/yolo
        ```

    - How to deploy private images is described here: https://docs.digitalocean.com/products/paperspace/deployments/how-to/manage-containers/

2.  The base image we're using in our Dockerfile has GPU support: https://github.com/amarder/deployolo/blob/main/Dockerfile#L1

3.  These lines in the Dockerfile instantiate a `YOLOV8Detector` object, when we do this the first time the required models are downloaded from the internet. It's nice to put this in the Dockerfile so the model files are included in the docker image and don't need to be downloaded from the internet every time we spin up a copy of this image: https://github.com/amarder/deployolo/blob/main/Dockerfile#L10C25-L12

Let me know if you have any questions.

To run locally use:

    docker compose up --build

This will automatically reload the code when it changes.