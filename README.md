
# This is a small container capable of sending Spark python scripts to a Spark master container running on k8s

### Usage

- Go to https://github.com/rodriguez-facundo/sparky and deploy the 2 files with Spark into your cluster.

- Find the kubectl config file (~/.kube/config in my mac). It looks somewhat like this (I hide some fields):

```
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: VERY_LONG_NONSENSE
    server: https://AN_IP_GOES_HERE
  name: A_NAME
contexts:
- context:
    cluster: A_NAME
    user: A_NAME
  name: A_NAME
current-context: A_NAME
kind: Config
preferences: {}
users:
- name: A_NAME
  user:
    auth-provider:
      config:
        access-token: AN_ACCESS_TOKEN
        cmd-args: config config-helper --format=json
        cmd-path: /google-cloud-sdk/bin/gcloud
        expiry: 2019-05-09T23:29:56Z
        expiry-key: '{.credential.token_expiry}'
        token-key: '{.credential.access_token}'
      name: gcp
``` 

- Ones you have that file, create a simple Spark job like this one:

```
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName('KubernetesSpark').setMaster('spark://YOUR_SERVER_IP:7077')

sc = SparkContext(conf=conf)

words = 'the quick brown fox jumps over the lazy dog the quick brown fox jumps over the lazy dog'

seq = words.split()
data = sc.parallelize(seq)
counts = data.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b).collect()
dict(counts)
sc.stop()
```

- Now:
    - Modify config.json to be aligned with your server (Spark namespace).
    - Modify job.py example to get your Spark Load Balancer IP (the one with 7077 port).

- Run jobs like this:

```
docker run -it \
    -v abs_path_to_local_config:/root/.kube/config DOCKER_IMAGE \   <-- kubectl credentials
    job.py                                                          <-- Spark job
```