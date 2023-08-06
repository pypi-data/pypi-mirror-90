import quinn
from pyspark.sql import functions as F

def with_clean_first_name(df):
    return df.withColumn(
        "clean_first_name",
        quinn.remove_non_word_characters(F.col("first_name"))
    )
