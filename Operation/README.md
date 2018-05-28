# Ansible Playbook : Server management


Ansible playbooks that installs collectd + influxdb + grafana to collect your server metrics and fluentd + elasticsearch + kibana for your system/application logs analyzing/monitoring

## Playbook Architect:
__Server metrics collection using (collectd + influxdb + grafana)__:

![alt text][logo]

[logo]: http://www.vishalbiyani.com/wp-content/uploads/2016/02/Slide2.jpg

(Image copied from internet via google search. From author of this topic http://www.vishalbiyani.com/graphing-performance-with-collectd-influxdb-grafana/ )

__Applications Logs collection using (fluentd + elasticsearch + kibana)__:

![alt text][logo1]

[logo1]: https://docs.fluentd.org/images/fluentd-elasticsearch-kibana.png


(Image copied from internet via google search from origin link https://docs.fluentd.org/v0.12/articles/free-alternative-to-splunk-by-fluentd)

## Requirements

You must have ansible installed on machine where you want to run this.

## Playbook description:
- Roles can find under __roles__ folder.
  - **collectd**: Install collectd on server to collect server metrics like cpu, mem, load, disk, io...
  - **docker**: Install docker-ce and docker-compose ( This role use most of the code from https://github.com/geerlingguy/ansible-role-docker )
  - **elasticsearch**: This role will create a single node elasticsearch cluster with kibana using docker
  - **fluentd**: This role will start a fluentd container which running fluentd agent to collectd logs and sent to elasticsearch 
  - **grafana**: Install and start grafana dashboard container, which included a scripted dashboard that auto generate stats for all servers. ( Scripted dashboard come with 3 js files, which I copied from unknown author as I got it before and just reuse it. It's been a while and I forgot the origin link after I made some small changes on the code. )
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

This playbook able to cover some basic server metrics and system/application logs for troubleshooting purpose. For additional metrics and applications logs you need to do more works. But it quit easy to do so

__Example__: 

- To add additional applications logs like apache logs you can easily changes **fluentd.j2** file from `fluentd` role by add more input type like below. 
```
# Collect apache logs

<source>
  @type tail
  path /var/log/httpd/access.log #...or where you placed your Apache access log
  pos_file /var/log/httpd/access.log.pos # This is where you record file position
  tag apache
  format apache2 # Do you have a custom format? You can write your own regex.
</source>

<match apache.**>
  @type copy
  <store>
    @type elasticsearch
    host {{ elasticsearch }}
    port {{ elasticsearch_port }}
    index_name {{ apache_es_index_name }}
    time_key @timestamp
    resurrect_after 5
    flush_interval 1s
  </store>
  <store apache.**>
    @type stdout
  </store>
</match>
```

You can remove 
```
  <store apache.**>
    @type stdout
  </store>
```
if you don't want to get log stdout to the console log.

- If you want to also monitor your database metrics for performance or applications query statistic long queries, slow queries...etc you can also use **collectd** to do that by using **https://collectd.org/wiki/index.php/Plugin:DBI* or **https://github.com/chrisboulton/collectd-python-mysql* which quit easy to tweak to match with your need.


