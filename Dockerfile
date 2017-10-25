FROM centos:centos7
MAINTAINER Mozilla Corporation Telemetry Pipeline team

# Install the appropriate software
RUN yum -y update; yum clean all
RUN yum -y install epel-release; yum clean all
RUN yum -y install wget gcc gcc-c++ cmake3 jq make; yum clean all

WORKDIR /downloads

# Old luasandbox-parquet version
RUN wget https://hsadmin.trink.com/packages/centos7/sprintAug21.tgz https://hsadmin.trink.com/packages/centos7/external/parquet-cpp-0.0.1-Linux.rpm
RUN tar xf sprintAug21.tgz; yum -y install luasandbox-1* luasandbox-parquet* parquet-cpp*; rm *.rpm

# New version for everything else
RUN wget https://hsadmin.trink.com/packages/centos7/all.tgz
RUN tar xf all.tgz
RUN yum -y install luasandbox-1* hindsight-0* luasandbox-lfs* luasandbox-lpeg* luasandbox-rjson* luasandbox-cjson*; yum clean all

COPY . /app

RUN rm -fr release/; mkdir release/

WORKDIR /app/release

RUN ln -s /usr/bin/cmake3 /usr/bin/cmake; cmake ..; make

CMD    ["ctest3", "-V", "-C", "hindsight"]
