FROM python:3.10

# Install dependencies
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . /app

ENTRYPOINT [ "flask", "run", "--host", "0.0.0.0" ]