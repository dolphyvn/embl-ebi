# Ansible Playbook : Server management


Ansible playbooks that installs some basic tools to collect server stats and logs

## Playbook Architect:
__Server metrics collection using (collectd + influxdb + grafana)__:

![alt text][logo]

[logo]: http://www.vishalbiyani.com/wp-content/uploads/2016/02/Slide2.jpg

(Image copied from internet via google search. From author of this topic http://www.vishalbiyani.com/graphing-performance-with-collectd-influxdb-grafana/ )

__Applications Logs collection using (fluentd + elasticsearch + kibana)__:

![alt text][logo1]

[logo1]: https://docs.fluentd.org/images/fluentd-elasticsearch-kibana.png


(Image copied from internet via google search via https://docs.fluentd.org/v0.12/articles/free-alternative-to-splunk-by-fluentd)

## Requirements

None.

## Playbook description:
- Roles can find under __roles__ folder.
  - **collectd**: Install collectd on server to collect server metrics like cpu, mem, load, disk, io...
  - **docker**: Install docker-ce and docker-compose
  - **elasticsearch**: This role will create a single node elasticsearch cluster with kibana using docker
  - **fluentd**: This role will start a fluentd container which running fluentd agent to collectd logs and sent to elasticsearch 
  - **grafana**: Install and start grafana dashboard container
  - **influxb**: Install and start an influxdb instance to receiving metrics from collectd
  - **rsyslog**: Install rsyslogs on server to collect system logs and send it to fluentd
- __inventory__ file: Storing your inventory. You should change and define your server group and ip accordingly
- __main.yaml__: is the main yaml file where you can decide which roles you want to run. Make sure you double check what role you want to install.


## Role Variables

Available variables can be changes under (`<role_name>/vars/main.yml`):

__Example__: ( grafana/vars/main.yaml )

```
---
influxdb_url: http://192.168.3.199:8086
grafana_url: http://192.168.3.199:3000
grafana_image_name: "dolphyvn/grafana"

```
You can find other variables on other roles and change accordingly

## Dependencies

None.

## How to run this playbook:

On machine where you have ansible installed just run:

`# ansible-playbook -i inventory main.yaml`

## How to use this playbook:

This playbook only containt basic software stack that setup for you a central management tools to manage server metrics and your server system logs. Details can find in each role. 
__Example__: 

If you already have an infrastructure where you also have grafana and influxdb running in order to get metrics for new server you should able to do it by change few variable from __inventory__ file where you should find influxdb setting
```
[all:vars]
elasticsearch="192.168.3.198"
elasticsearch_port="9200"
rsyslog_es_index_name="rsyslog"
influxdb="192.168.3.199"
influxdb_port="25826"
fluentd_host="192.168.3.198"
fluentd_port="5140"
```
You should change `influxdb` and `influxdb_host` to your setting respectivily 
How to add additional applications logs:
How to add additional database logs
How to add additional database metrics

## Example Playbook

```yaml
- hosts: all
  roles:
    - geerlingguy.docker
```

