# --platform=linux/amd64 added to prevent pulling ARM images when run on Apple Silicon
FROM --platform=linux/amd64 python:3.11-slim-bookworm
LABEL maintainer="Mozilla Data Platform"

# copied from library/rust:1.73.0-slim-bullseye to install rust >= 1.65 and cargo >= 0.57 needed to build jsonschema-transpiler
# https://github.com/rust-lang/docker-rust/blob/97a7686492c0ef95717f3f5e93ee24186a407329/1.73.0/bullseye/slim/Dockerfile#L3-L37
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.98.1

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        gcc \
        libc6-dev \
        wget \
        ; \
    rustArch='x86_64-unknown-linux-gnu'; \
    rustupSha256='dda7234360b7f578ca8b0ddcb80145646fa61a67c1720a5abc7051b35c9fcb71' ; \
    url="https://static.rust-lang.org/rustup/archive/1.29.1/${rustArch}/rustup-init"; \
    wget "$url"; \
    echo "${rustupSha256} *rustup-init" | sha256sum -c -; \
    chmod +x rustup-init; \
    ./rustup-init -y --no-modify-path --profile minimal --default-toolchain $RUST_VERSION --default-host ${rustArch}; \
    rm rustup-init; \
    chmod -R a+w $RUSTUP_HOME $CARGO_HOME; \
    rustup --version; \
    cargo --version; \
    rustc --version; \
    apt-get remove -y --auto-remove \
        wget \
        ; \
    rm -rf /var/lib/apt/lists/*;

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
        openjdk-17-jdk-headless \
        maven

# Install jsonschema-transpiler
ENV PATH=$PATH:/root/.cargo/bin
RUN cargo install jsonschema-transpiler --version 2.0.1

# Configure git for testing
RUN git config --global user.email "mozilla-pipeline-schemas@mozilla.com"
RUN git config --global user.name "Mozilla Pipeline Schemas"

WORKDIR /app

COPY --from=mozilla/ingestion-sink:latest /app/ingestion-sink/target /app/target

# Install python dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip3 install --upgrade pip setuptools==70.3.0 && \
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
