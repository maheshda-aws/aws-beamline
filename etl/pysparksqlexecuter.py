import sys
from datetime import datetime
from optparse import OptionParser
from pyspark.sql.functions import *
from pyspark.sql import SparkSession


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-s", "--sql_location", type="string", dest="sql_file_location",
                      help="location file location in S3")
    parser.add_option("-i", "--job_config", type="string", dest="job_config",
                      help="Job config file")
    (options, args) = parser.parse_args()



    print(len(sys.argv))
    if (len(sys.argv) != 3):
        print("Usage: spark-etl [input-folder] [output-folder]")
        sys.exit(0)

    spark = SparkSession \
        .builder \
        .appName("SparkETL") \
        .getOrCreate()

    nyTaxi = spark.read.option("inferSchema", "true").option("header", "true").csv(sys.argv[1])

    updatedNYTaxi = nyTaxi.withColumn("current_date", lit(datetime.now()))

    updatedNYTaxi.printSchema()

    print(updatedNYTaxi.show())

    print("Total number of records: " + str(updatedNYTaxi.count()))

    updatedNYTaxi.write.parquet(sys.argv[2])