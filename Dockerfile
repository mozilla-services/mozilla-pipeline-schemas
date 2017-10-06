FROM centos:centos7
MAINTAINER Mozilla Corporation Telemetry Pipeline team

# Install the appropriate software
RUN yum -y update; yum clean all
RUN yum -y install epel-release; yum clean all
RUN yum -y install cmake3 cmake jq make luasandbox hindsight luasandbox-lfs luasandbox-lpeg luasandbox-rjson luasandbox-cjson luasandbox-parquet; yum clean all

WORKDIR /app/release
COPY . /app

RUN cmake3 ..; cpack -G TGZ; make
CMD    ["ctest", "-V", "-C", "hindsight"]
