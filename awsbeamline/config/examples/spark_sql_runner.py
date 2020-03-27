import sys
import yaml
import logging
import subprocess
from argparse import ArgumentParser
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import *


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def main():

    parser = ArgumentParser(description="Commandline for executing SQL in spark")
    parser.add_argument("-i", "--instanceId",
                      dest="instance_id",
                      help="Task instance identifier")
    parser.add_argument("-s", "--sqlLocation",
                      dest="sql_location",
                      help="SQL file location in S3")
    parser.add_argument("-o", "--outputLocation",
                      dest="output_location",
                      help="Result output location in S3")
    parser.add_argument("-f", "--outputFormat",
                      dest="output_format",
                      help="Result output format in S3")

    args = parser.parse_args()

    logging.info("Arguments provided: {}".format(args))
    logging.info("Downloading config file and sql file to /tmp.")
    sql_instance_file = "/tmp/{}.sql".format(args.instance_id)
    subprocess.run(["aws", "s3", "cp", args.sql_location, sql_instance_file])
    logging.info("Starting spark SQL session.")
    spark = SparkSession \
        .builder \
        .appName("PythonSparkSQL") \
        .enableHiveSupport() \
        .getOrCreate()
    logging.info("Reading sql file at location: {}.".format(sql_instance_file))
    sql_file = open(sql_instance_file, mode='r')
    sql = sql_file.read()
    sqlDF = spark.sql(sql)
    logging.info(sqlDF.show())
    logging.info("Writing output to location: {},  format: {}.".format(args.output_location, args.output_format))
    sqlDF.write.format(args.output_format).mode('overwrite').save(args.output_location)
    logging.info("Output successfully written. Stoping spark session.")
    spark.stop()

if __name__ == "__main__":
    main()