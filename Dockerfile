FROM tensorflow/tensorflow:latest-gpu

# Install dependencies
RUN python3 -m pip install --upgrade pip
RUN pip install --ignore-installed blinker
RUN pip install keras-cv Flask

WORKDIR /app

COPY download.py /app/download.py
RUN python download.py

# Copy the rest of the code
COPY . /app

ENTRYPOINT [ "flask", "run", "--host", "0.0.0.0" ]
# ENTRYPOINT [ "bash" ]
