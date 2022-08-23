# debian bullseye provides rust >= 1.46 needed to build jsonschema-transpiler
# --platform=linux/amd64 added to prevent pulling ARM images when run on Apple Silicon
FROM --platform=linux/amd64 debian:bookworm-slim
LABEL maintainer="Mozilla Data Platform"

# man directory is removed in upstream debian:slim, but needed by jdk install
RUN mkdir -p /usr/share/man/man1 && \
    apt-get update -qqy && \
    apt-get install -qqy \
        cmake \
        diffutils \
        gcc \
        g++ \
        jq \
        make \
        wget \
        git \
        openjdk-11-jdk-headless \
        maven \
        cargo \
        python3-pip

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
