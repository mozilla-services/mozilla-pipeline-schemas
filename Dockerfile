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
    && dnf clean all

WORKDIR /downloads

# Install hindsight and the luasandbox
RUN wget -qO- https://s3-us-west-2.amazonaws.com/net-mozaws-data-us-west-2-ops-ci-artifacts/mozilla-services/lua_sandbox_extensions/master/centos7/all.tgz | tar xvz
RUN wget https://s3-us-west-2.amazonaws.com/net-mozaws-data-us-west-2-ops-ci-artifacts/mozilla-services/lua_sandbox_extensions/external/centos7/parquet-cpp-1.3.1-1.x86_64.rpm

RUN dnf -y install \
    hindsight-0* \
    luasandbox-1* \
    luasandbox-cjson* \
    luasandbox-lfs* \
    luasandbox-lpeg* \
    luasandbox-parquet* \
    luasandbox-rjson* \
    parquet-cpp* \
    && dnf clean all

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
RUN mvn dependency:copy-dependencies

RUN rm -fr /app/release; mkdir /app/release
WORKDIR /app/release
RUN cmake ..; make

WORKDIR /app
CMD pytest -v
