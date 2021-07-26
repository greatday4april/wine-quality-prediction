FROM python:3
WORKDIR /app

# Install OpenJDK-11
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

EXPOSE 80
ENTRYPOINT ["python3", "prediction-app.py"]
