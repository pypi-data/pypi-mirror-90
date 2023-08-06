import socket
from pyspark.sql import SparkSession
import pandas as pd
from parseudr.convertfqdntoip import returnips


class getfqdnips:
    def donslookup():
        spark = SparkSession.builder.getOrCreate()
        url = "https://docs.microsoft.com/en-us/azure/databricks/administration-guide/cloud-configurations/azure/udr"
        df = pd.read_html(url, header=0)[2]
        pdf1 = df.assign(
            FQDN=df["FQDN"].str.replace("net", "net\n").str.split("\n")
        ).explode("FQDN")
        pdf2 = pdf1.assign(
            FQDN=pdf1["FQDN"].str.replace("com", "com\n").str.split("\n")
        ).explode("FQDN")
        pdf2 = pdf2[pdf2["FQDN"] != ""]
        pdf2["IPAddress"] = pdf2["FQDN"].map(
            lambda host: returnips.tryconvert(host) if host is not None else host
        )
        sdf = spark.createDataFrame(pdf2)
        sdf.createOrReplaceTempView("UDR")
        return sdf