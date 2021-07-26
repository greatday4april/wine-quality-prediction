# wine-quality-prediction

## Summary

1. Github: https://github.com/greatday4april/wine-quality-prediction
2. Docker image link: https://hub.docker.com/layers/jialinjit/wine-quality-prediction/v1/images/sha256:ab1e5ec8451860b36fde549cb2837c1fcac03aca3e68c7cdafc424b341f9643a

To run the docker, assume the test data file name is `TestingDataset.csv`, then after cd into the folder contains the test data file
`sudo docker run -v "$(pwd)":/data jialinjit/wine-quality-prediction:v1 /data/TestingDataset.csv`

(this mounts the folder as `/data` in container and run the script against `/data/TestingDataset.csv`)

### Without docker

1. Clone the repository and install java if hasn't
2. `pip3 install -r requirements.txt`
3. `python3 prediction-app.py TestingDataset.csv`

## Training Result

Based on validation data

```bash
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
F1 score on validation data = 0.542471
```

## Setup

1. Download prebuilt spark https://www.apache.org/dyn/closer.lua/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz and extract to home folder as `spark` folder
2. `pip install pyspark`
3. `brew install flintrock` as better alternative to `spark-ec2`
4. Create or download existing keypair as `~/.ssh/jia-li.pem`

## Train model

Use `flintrock` to launch cluster and run spark, which is a newer alternative to `spark-ec2`

1. `flintrock configure` and set params:

```yaml
services:
  spark:
    version: 3.1.2
  hdfs:
    version: 3.3.0

provider: ec2

providers:
  ec2:
    key-name: jia-li
    identity-file: /Users/james/.ssh/jia-li.pem
    instance-type: t2.micro
    region: us-east-1
    # availability-zone: <name>
    ami: ami-0dc2d3e4c0f9ebd18
    user: ec2-user
    tenancy: default  # default | dedicated
    ebs-optimized: no  # yes | no
    instance-initiated-shutdown-behavior: terminate  # terminate | stop

launch:
  num-slaves: 3
debug: false
```

2. `flintrock launch test-cluster` to launch cluster of 4 instances

3. Here we use `spark.ml` package the new dataframe-based APIs: https://spark.apache.org/docs/latest/api/python/reference/pyspark.ml.html

4. Follow https://towardsdatascience.com/building-a-linear-regression-with-pyspark-and-mllib-d065c3ba246a to do initial attempt for training model and then try other classifiers as well as tune parameters

5. Copy code and data to cluster
  - `flintrock copy-file test-cluster prediction.py /home/ec2-user/prediction.py`
  - `flintrock copy-file test-cluster TrainingDataset.csv /home/ec2-user/TrainingDataset.csv`
  - `flintrock copy-file test-cluster ValidationDataset.csv /home/ec2-user/ValidationDataset.csv`

6. `flintrock login test-cluster` to login into the cluster

7. `pip3 install pyspark` and `pip3 install numpy`

8. `python3 prediction.py` in cluster

9. download exported model to local directory

## Prediction App

1. Install docker https://docs.docker.com/docker-for-mac/install/
2. Create `Dockerfile` with dependency install
3. `sudo docker build -t wine-quality-prediction .`
4. cd into the folder contains the data file, assume the data file name is `TestingDataset.csv`, then
`sudo docker run -v "$(pwd)":/data wine-quality-prediction /data/TestingDataset.csv`
