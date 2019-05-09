FROM alpine:3.9

# RUN:
#
#      docker run -it -v local-kube-config:/root/.kube/config IMAGE_NAME script.py



# gcloud sdk
ARG CLOUD_SDK_VERSION=245.0.0
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION

ENV PATH /google-cloud-sdk/bin:$PATH
RUN apk --no-cache add \
        curl \
        python3 \
        py-crcmod \
        bash \
        libc6-compat \
        openssh-client \
        git \
        gnupg \
    && curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    tar xzf google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    rm google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz && \
    ln -s /lib /lib64 && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true && \
    gcloud config set metrics/environment github_docker_image && \
    gcloud --version

# Kubectl
RUN apk update && apk add ca-certificates && apk add openssl && rm -rf /var/cache/apk/*
RUN adduser -S gkh gkh
RUN gcloud components install docker-credential-gcr -q --no-user-output-enabled
RUN gcloud components install kubectl -q --no-user-output-enabled
RUN mkdir -p /root/.kube
WORKDIR /home/gkh

# Spark scripts
COPY kubectl.py /home/gkh/kubectl.py 
COPY config.json /home/gkh/config.json 

ENTRYPOINT ["python3", "kubectl.py"]

