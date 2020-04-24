FROM centos:centos8
LABEL maintainer="Firefox Data Platform"

# Install the appropriate software
RUN dnf -y update && \
    dnf -y install epel-release && \
    dnf -y install \
        cmake3 \
        gcc \
        gcc-c++ \
        jq \
        make \
        which \
        wget \
        git \
        python36 \
        java-1.8.0-openjdk-devel \
        maven \
        cargo \
    && dnf clean all

ENV PATH=$PATH:/root/.cargo/bin
RUN cargo install jsonschema-transpiler --version 1.8.0
# Configure git for testing
RUN git config --global user.email "mozilla-pipeline-schemas@mozilla.com"
RUN git config --global user.name "Mozilla Pipeline Schemas"

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
RUN mvn dependency:copy-dependencies

RUN rm -rf /app/release && \
    mkdir /app/release && \
    cd release && \
    cmake .. && \
    make

WORKDIR /app
CMD pytest -v
