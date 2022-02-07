FROM centos:centos8.4.2105
LABEL maintainer="Mozilla Data Platform"

# Install the appropriate software
# Must migrate from centos 8 to centos stream-8 before updating repos
# because centos 8 hit EOL on 2021-12-31
RUN echo 'fastestmirror=1' >> /etc/dnf/dnf.conf && \
    dnf -y --disablerepo '*' --allowerasing install \
        http://mirror.centos.org/centos/8-stream/BaseOS/x86_64/os/Packages/{centos-stream-release-8.6-1,centos-stream-repos-8-4,centos-gpg-keys-8-4}.el8.noarch.rpm && \
    dnf -y distro-sync && \
    dnf -y update && \
    dnf -y install epel-release && \
    dnf -y install \
        cmake \
        diffutils \
        gcc \
        gcc-c++ \
        jq \
        make \
        which \
        wget \
        git \
        python36 \
        java-11-openjdk-devel \
        maven \
        cargo \
    && dnf clean all

# ensure we're actually using java 11
ENV JAVA_HOME=/etc/alternatives/java_sdk_11_openjdk
RUN alternatives --set java `readlink $JAVA_HOME`/bin/java

# Install jsonschema-transpiler
ENV PATH=$PATH:/root/.cargo/bin
RUN cargo install jsonschema-transpiler --version 1.9.0

# Configure git for testing
RUN git config --global user.email "mozilla-pipeline-schemas@mozilla.com"
RUN git config --global user.name "Mozilla Pipeline Schemas"

WORKDIR /app

COPY --from=mozilla/ingestion-sink:latest /app/ingestion-sink/target /app/target

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
