FROM solr:6.5.0

COPY ./. /home/

EXPOSE 8984
WORKDIR /opt/solr

RUN mkdir -p /opt/solr/server/solr/mycores/searcher && \
  mkdir -p /opt/solr/server/solr/mycores/pdf && \
  bin/solr start && \
  bin/solr create -c searcher && \
  bin/solr create -c pdf && \
  bin/solr stop -all && \
  mkdir -p /opt/solr/server/solr/searcher/conf/mapping && \
  mkdir -p /opt/solr/server/solr/pdf/conf/mapping && \
  cp -f /home/searcher/conf/*.txt /opt/solr/server/solr/searcher/conf/ && \
  cp -f /home/searcher/conf/mapping/*.txt /opt/solr/server/solr/searcher/conf/mapping/ && \
  cp -f /home/searcher/conf/solrconfig.xml /opt/solr/server/solr/searcher/conf/solrconfig.xml && \
  cp -f /home/searcher/core/core.properties /opt/solr/server/solr/searcher/core.properties && \
  cp -f /home/searcher/schema.xml /opt/solr/server/solr/searcher/schema.xml && \
  cp -f /home/pdf/conf/*.txt /opt/solr/server/solr/pdf/conf/ && \
  cp -f /home/pdf/conf/mapping/*.txt /opt/solr/server/solr/pdf/conf/mapping/ && \
  cp -f /home/pdf/conf/solrconfig.xml /opt/solr/server/solr/pdf/conf/solrconfig.xml && \
  cp -f /home/pdf/core/core.properties /opt/solr/server/solr/pdf/core.properties && \
  cp -f /home/pdf/schema.xml /opt/solr/server/solr/pdf/schema.xml 