FROM tensorflow/tensorflow:latest-gpu

# Install dependencies
WORKDIR /app

RUN python3 -m pip install --upgrade pip
RUN pip install --ignore-installed blinker==1.7.0

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY download.py /app/download.py
RUN python download.py

# Copy the rest of the code
COPY . /app

ENTRYPOINT [ "flask", "run", "--host", "0.0.0.0" ]