from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.classification import RandomForestClassifier as classifier
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler


def dataframe_from_file(session, path):
    df = session.read.csv(path, inferSchema=True, sep=";", header=True)

    feature_list = []
    label_col = None
    for name in df.columns:
        if 'quality' in name:
            label_col = name
        else:
            feature_list.append(name)

    assembler = VectorAssembler(
        inputCols=feature_list, outputCol="features")
    train_df = assembler.transform(df)
    return train_df.withColumnRenamed(label_col, "label").select('features', 'label')


if __name__ == "__main__":
    conf = SparkConf().setAppName('wine-quality').setMaster('local[*]').set('spark.executor.memory', '4g').set('spark.driver.memory', '20g')
    sc = SparkContext(conf=conf)
    spark = SparkSession(sc)

    train_df = dataframe_from_file(sc, "TrainingDataset.csv")

    cf = classifier(featuresCol='features', labelCol='label', numTrees=2000, maxBins=10)
    model = cf.fit(train_df)
    model.write().overwrite().save('output/cf.model')

    test_df = dataframe_from_file(sc, "ValidationDataset.csv")
    predictions = model.transform(test_df).withColumn("label", col("label").cast("double")).select("label", "prediction")
    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction", labelCol="label", metricName="f1")
    print("F1 score on validation data = %g" % evaluator.evaluate(predictions))
