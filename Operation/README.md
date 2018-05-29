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
- Action plugins folder: This action plugin will create a templating dashboard for all running server with basic metrics like cpu/memory/load/disk space

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

__Use fluentd for logs collection__: 

- To add additional applications logs like apache logs you can easily modify **fluentd.j2** file from `fluentd` role by add more input type like below. 
```
# Collect apache logs

<source>
  @type tail
  path /var/log/httpd/access.log #...or where you placed your Apache access log
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
- If you want to collect your custom application like java,python,php you can do the same above but you might need to create your own custom file format.
```
<source>
  @type tail
  path /var/log/applications/app.log #...or where you placed your application log
  tag custom_application
  format custom_regex
  custom_regex <> # Put your regex inside <> tag
</source>

<match custom_application.**>
  @type copy
  <store>
    @type elasticsearch
    host {{ elasticsearch }}
    port {{ elasticsearch_port }}
    index_name {{ custom_es_index_name }} # You should define this variable in vars/main.yaml file or just insert directly
    time_key @timestamp
    resurrect_after 5
    flush_interval 1s
  </store>
</match>
```
__Use collectd + influxdb + grafana to collect server metrics and visualize it__:

- *How to access scripted dashboard* : 
   - After grafana started please head to url: **http://{{grafana_url}}:3000** and login with user/pass default admin/admin
   - To go to a specific server dashboard : **http://{{grafana_url}}:3000/dashboard/script/getdash.js?host=hostname** ( replace hostname with your server hostname )
   - Or if you want to stack two dashboard side by side: (hostname1 and hostname2) **http://{{grafana_url}}:3000/dashboard/script/getdash.js?host=hostname(1|2)&span=6**
   - Or you only want to display special metrics: **http://{{grafana_url}}:3000/dashboard/script/getdash.js?host=hostname(1|2)&span=6&metric=cpu,load,memory**

- Templating dashboard can access via "**Main Dashboard**" at home page. ( You can search for it, usually it will appear after you login )
  - To make the import for templating works properly you need to define hostname in the inventory file.
  ```
  [nodes]
  node1 ansible_ssh_host=192.168.3.198
  node2 ansible_ssh_host=192.168.3.199
  node3 ansible_ssh_host=192.168.3.200
  ```
  - Please aware that group nodes has to be the same, unless you want to change it you also need to change in `grafana_import.py` in action_plugins folder ( line 39 )
     ```
     39       nodes = task_vars["groups"]["nodes"]
     ```
     ( It's better to get all server hostname via database, because sometime you want to automated your inventory files as well. This is just a quick dirty hack. )
     
- If you want to also monitor your database metrics for performance or applications query statistic long queries, slow queries you can also you **collectd** to do that by using **https://collectd.org/wiki/index.php/Plugin:DBI** or **https://github.com/chrisboulton/collectd-python-mysql** which quit easy to tweak to match with your need.
