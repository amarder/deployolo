FROM tensorflow/tensorflow:latest-gpu

WORKDIR /app

# Install dependencies
# RUN pip install --ignore-installed blinker==1.7.0
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Download the model
COPY main.py /app/main.py
RUN python main.py

# Copy the rest of the code
COPY . /app

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
