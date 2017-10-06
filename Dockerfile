FROM centos:centos7
MAINTAINER Mozilla Corporation Telemetry Pipeline team

# Install the appropriate software
RUN yum -y update; yum clean all
RUN yum -y install epel-release; yum clean all
RUN yum -y install git gcc gcc-c++ cmake3 jq make boost-devel openssl-devel flex bison libtool; yum clean all

WORKDIR /git

# Lua Sandbox
RUN git clone https://github.com/mozilla-services/lua_sandbox.git
RUN cd lua_sandbox; mkdir release; cd release; cmake3 -DCMAKE_BUILD_TYPE=release ..; make; make install

# hindsight
RUN git clone https://github.com/mozilla-services/hindsight.git
RUN cd hindsight; mkdir release; cd release; cmake3 -DCMAKE_BUILD_TYPE=release ..; make; make install

# parquet-ccp
RUN git clone https://github.com/apache/parquet-cpp.git
RUN cd parquet-cpp; cmake3 .; make; make install

# luasandbox-extensions
RUN git clone https://github.com/mozilla-services/lua_sandbox_extensions.git
RUN cd lua_sandbox_extensions; mkdir release; cd release; cmake3 -DCMAKE_BUILD_TYPE=release -DEXT_lpeg=on -DEXT_lfs=on -DEXT_heka=on -DEXT_rjson=on -DEXT_cjson=on ..; make; make install

COPY . /app
RUN rm -fr release/; mkdir release/
WORKDIR /app/release

RUN cmake3 ..; make

CMD    ["ctest3", "-V", "-C", "hindsight"]
