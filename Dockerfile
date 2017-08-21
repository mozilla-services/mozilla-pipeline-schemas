FROM mozilla/hindsight

USER root
RUN yum -y install \
    cmake3 \
    jq \
    make \
    && yum -y clean all

COPY . /schemas
RUN chown -R app:app /schemas

USER app
RUN mkdir /schemas/release
WORKDIR /schemas/release

RUN cmake -Wno-dev .. && \
    cpack -G TGZ

CMD make && ctest -V -C hindsight
