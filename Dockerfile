FROM centos:centos7
LABEL maintainer="Firefox Data Platform"

# Install the appropriate software
RUN yum -y update && \
    yum -y install epel-release && \
    yum -y install \
        cmake3 \
        gcc \
        gcc-c++ \
        jq \
        make \
        wget \
        python-pip \
    && yum clean all

RUN pip install jsonschema

WORKDIR /downloads

# Install hindsight and the luasandbox
RUN wget -qO- https://hsadmin.trink.com/packages/centos7/all.tgz | tar xvz
RUN wget https://hsadmin.trink.com/packages/centos7/external/parquet-cpp-1.3.1-1.x86_64.rpm
RUN yum -y install \
    hindsight-0* \
    luasandbox-1* \
    luasandbox-cjson* \
    luasandbox-lfs* \
    luasandbox-lpeg* \
    luasandbox-parquet* \
    luasandbox-rjson* \
    parquet-cpp* \
    && yum clean all

COPY . /app

RUN rm -fr release/; mkdir release/

WORKDIR /app/release

RUN ln -s /usr/bin/cmake3 /usr/bin/cmake; cmake ..; make

CMD python test_schema_format.py ../schemas && ctest3 -V -C hindsight
