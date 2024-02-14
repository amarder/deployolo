1.  Get the code and build the docker image.

        git clone https://github.com/amarder/deployolo.git
        cd deployolo
        docker build . -t yolo

    I'm not sure if this `docker build` command will use the GPU by default.

2.  Run the docker container:

        docker run --gpus all -p 5000:5000 yolo

3.  Test the container by going to http://localhost:5000/ and uploading a jpg image. After it finishes processing go to http://localhost:5000/nvidia-smi/ to see if it's using the GPU.