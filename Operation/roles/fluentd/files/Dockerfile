from fluent/fluentd
COPY fluentd.conf /fluentd/etc/
RUN gem install fluent-plugin-elasticsearch
CMD exec fluentd -c /fluentd/etc/${FLUENTD_CONF} -p /fluentd/plugins $FLUENTD_OPT
