# -*-coding:utf-8 -*-
import os
import argparse
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F

from UCF import *


def parse_argvs():
    parser = argparse.ArgumentParser(description='[collaborativeFiltering]')
    parser.add_argument("--data_path", type=str, default='./ratings.csv')
    args = parser.parse_args()
    print('[input params] {}'.format(args))

    return parser, args


if __name__ == '__main__':
    parser, args = parse_argvs()
    data_path = args.data_path
    model_path = args.model_path
    train_flag = args.train_flag
    epoch = args.epoch

    conf = SparkConf().setAppName('collaborativeFiltering').setMaster("local[*]")
    spark_session = SparkSession.builder.config(conf=conf).getOrCreate()

    # read data
    data_path = os.path.abspath(data_path)
    data_path = "file://" + data_path
    print("[spark] read file path: {}".format(data_path))

    ratingSamples = spark_session.read.format('csv').option('header', 'true').load(data_path) \
        .withColumn("userIdInt", F.col("userId").cast(IntegerType())) \
        .withColumn("movieIdInt", F.col("movieId").cast(IntegerType())) \
        .withColumn("ratingFloat", F.col("rating").cast(FloatType()))
    training, test = ratingSamples.randomSplit((0.8, 0.2), seed=2022)

    # collaborative filtering start
    cf = UCF(training, k=100, n=10000, spark_session=spark_session)

    user_recs = cf.getrecommandList()
    user_recs.coalesce(1) \
        .write.mode("overwrite") \
        .option("header", "true") \
        .csv("./recommend")

    spark_session.stop()
