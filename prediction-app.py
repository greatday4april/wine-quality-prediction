import pyspark
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from prediction import dataframe_from_file
from pyspark.sql.functions import col
import json

import sys

session = pyspark.sql.SparkSession.builder.appName(
    'wine-quality').getOrCreate()
trainedModel = RandomForestClassificationModel.load("./output/cf.model")

print("loading file: {}".format(sys.argv[1]))
df = dataframe_from_file(session, sys.argv[1])

predictions = trainedModel.transform(df).withColumn(
    "label", col("label").cast("double")).select("label", "prediction")
evaluator = MulticlassClassificationEvaluator(
    predictionCol="prediction", labelCol="label", metricName="f1")

print("predictions:")
print(json.dumps([x['prediction'] for x in predictions.collect()]))
print("F1 score on validation data = %g" % evaluator.evaluate(predictions))
