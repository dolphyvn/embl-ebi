from grafana/grafana

COPY getdash.app.js getdash.conf.js /usr/share/grafana/public/app/
COPY getdash.js /usr/share/grafana/public/dashboards/
ENTRYPOINT ["/run.sh"]
