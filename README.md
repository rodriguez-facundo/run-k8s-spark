
# This is a small container capable of sending Spark python scripts to a Spark master container running on k8s

### Usage
If you don't want to use the docker, a simple  `python kubectl.py job.py` will send the job from your local machine if kubectl has access to the cluster. 

Otherwise:

- If you don't have a k8s Spark deplyment, go to https://github.com/rodriguez-facundo/sparky.

- Now we need to find the kubectl credentials in your local machine (~/.kube/config in mine). It should look somewhat like this (I hide some fields):

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

- Now:
    - Modify config.json to be aligned with your server (Spark namespace).
    - Modify job.py example to get your Spark Load Balancer IP (the one with 7077 port).

- Run:
    - `docker build -t send-spark-job .` to build a docker image.

- Run jobs like this:

```
docker run -it \
    -v abs_path_to_local_config:/root/.kube/config DOCKER_IMAGE \   <-- kubectl credentials
    send-spark-job                                                  <-- Image you just built
    job.py                                                          <-- Spark job
```