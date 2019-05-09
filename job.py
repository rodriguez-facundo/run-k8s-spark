from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName('KubernetesSpark').setMaster('spark://YOUR_SERVER_IP:7077')

sc = SparkContext(conf=conf)

words = 'the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog'

seq = words.split()
data = sc.parallelize(seq)
counts = data.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).collect()
dict(counts)
sc.stop()
