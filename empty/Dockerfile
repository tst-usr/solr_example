FROM solr:6.5.0

COPY ./. /home/

EXPOSE 8984
WORKDIR /opt/solr

RUN mkdir -p /opt/solr/server/solr/mycores/searcher && \
  bin/solr start && \
  bin/solr create -c searcher