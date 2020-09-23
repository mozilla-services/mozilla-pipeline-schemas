FROM centos:centos8.1.1911
LABEL maintainer="Firefox Data Platform"

# Install the appropriate software
RUN dnf -y update && \
    dnf -y install epel-release && \
    dnf -y install \
        cmake3 \
        diffutils \
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

# Install jsonschema-transpiler
ENV PATH=$PATH:/root/.cargo/bin
RUN cargo install jsonschema-transpiler --version 1.8.0

# Configure git for testing
RUN git config --global user.email "mozilla-pipeline-schemas@mozilla.com"
RUN git config --global user.name "Mozilla Pipeline Schemas"

WORKDIR /app

# Install python dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip3 install --upgrade pip setuptools && \
    pip3 install -r requirements.txt -r requirements-dev.txt

# Install Java dependencies
COPY pom.xml .
RUN mvn dependency:copy-dependencies

COPY . /app

RUN pip3 install .
RUN mkdir release && \
    cd release && \
    cmake .. && \
    make

CMD pytest -v
