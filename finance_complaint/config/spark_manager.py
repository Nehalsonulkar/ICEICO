from dotenv import load_dotenv
import os
from pyspark.sql import SparkSession

# Load environment variables from .env file
load_dotenv()

# Get AWS credentials from environment variables
AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"  # Replace with your environment key name if different
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"  # Replace with your environment key name if different

access_key_id = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY, "default_access_key_id")  # Default value if env var is not found
secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY, "default_secret_access_key")  # Default value if env var is not found

# Create Spark session
spark_session = SparkSession.builder.master('local[*]').appName('finance_complaint') \
    .config("spark.executor.instances", "1") \
    .config("spark.executor.memory", "6g") \
    .config("spark.driver.memory", "6g") \
    .config("spark.executor.memoryOverhead", "8g") \
    .config('spark.jars.packages', "com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.3") \
    .getOrCreate()

# Configure Hadoop for AWS S3
spark_session._jsc.hadoopConfiguration().set("fs.s3a.awsAccessKeyId", access_key_id)
spark_session._jsc.hadoopConfiguration().set("fs.s3a.awsSecretAccessKey", secret_access_key)
spark_session._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")  # Use S3AFileSystem
spark_session._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
spark_session._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.BasicAWSCredentialsProvider")
spark_session._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "ap-south-1.amazonaws.com")
spark_session._jsc.hadoopConfiguration().set("fs.s3.buffer.dir", "tmp")

# Spark session is ready to use
print("Spark session created successfully.")
