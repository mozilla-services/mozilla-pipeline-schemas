# --platform=linux/amd64 added to prevent pulling ARM images when run on Apple Silicon
FROM --platform=linux/amd64 python:3.8-slim-bullseye
LABEL maintainer="Mozilla Data Platform"

# copied from library/rust:1.63.0-slim-bullseye to install rust >= 1.46 and cargo >= 0.57 needed to build jsonschema-transpiler
# https://github.com/rust-lang/docker-rust/blob/2301a502c3ff8bbf30c32a6ef2114f3b363c4553/1.63.0/bullseye/slim/Dockerfile#L3-L37
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    RUST_VERSION=1.63.0

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        gcc \
        libc6-dev \
        wget \
        ; \
    dpkgArch="$(dpkg --print-architecture)"; \
    case "${dpkgArch##*-}" in \
        amd64) rustArch='x86_64-unknown-linux-gnu'; rustupSha256='5cc9ffd1026e82e7fb2eec2121ad71f4b0f044e88bca39207b3f6b769aaa799c' ;; \
        armhf) rustArch='armv7-unknown-linux-gnueabihf'; rustupSha256='48c5ecfd1409da93164af20cf4ac2c6f00688b15eb6ba65047f654060c844d85' ;; \
        arm64) rustArch='aarch64-unknown-linux-gnu'; rustupSha256='e189948e396d47254103a49c987e7fb0e5dd8e34b200aa4481ecc4b8e41fb929' ;; \
        i386) rustArch='i686-unknown-linux-gnu'; rustupSha256='0e0be29c560ad958ba52fcf06b3ea04435cb3cd674fbe11ce7d954093b9504fd' ;; \
        *) echo >&2 "unsupported architecture: ${dpkgArch}"; exit 1 ;; \
    esac; \
    url="https://static.rust-lang.org/rustup/archive/1.25.1/${rustArch}/rustup-init"; \
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
        openjdk-11-jdk-headless \
        maven

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
