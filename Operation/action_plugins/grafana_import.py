#!/usr/bin/env python

# (c) Copyright 2016 Cloudera, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import requests
import json
import os
from jinja2 import Environment, FileSystemLoader
import time
from ansible.plugins.action import ActionBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display

    display = Display()


class ActionModule(ActionBase):
    """ Generating dashboard """
    def run(self, tmp=None, task_vars=None):
      if task_vars is None:
          task_vars = dict()

      result = super(ActionModule, self).run(tmp, task_vars)

      nodes = task_vars["groups"]["nodes"]
      grafana_ip = task_vars["groups"]["grafana"][0]
      token = self.create_token(grafana_ip)
      res = self.create_dashboard(nodes,grafana_ip,token)
      
      if len(nodes) == 0:
        result['failed'] = True
        result['msg'] = "No hosts defined"
        return result
      elif res==200:
        result['failed'] = False
        result['msg'] = "Success imported dashboard"
        return result
      else:
        result['failed'] = True
        result['msg'] = "Can not import dashboard"
        return result

    def templating(self,servers):

      selected_server = servers[0]


      query = ""
      lists = []
      option = []
      variable = { "allValue": "null",
                   "current": {
                      "tags": [],
                      "text": "{}".format(selected_server),
                      "value": "{}".format(selected_server)
                    },
                    "hide": 0,
                    "includeAll": False,
                    "label": "Instance",
                    "multi": False,
                    "name": "server",
                    "type": "custom"
                  }

      for server in servers:
        query = query + "," + server
        item = {"selected": False,"text": server,"value": server}
        option.append(item)

      variable['options'] = option
      variable['query']  = query
      return DictConvert(variable)

    def dashboard_render(self,servers):
      """ Render dashboard from template """
      THIS_DIR = os.path.dirname(os.path.abspath(__file__))
      j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
      new_dashboard = (j2_env.get_template('templating_dashboard.json').render(
                list_templating=self.templating(servers)
          ))
      return (new_dashboard)

    def create_dashboard(self,servers,grafana_ip,token):
      """ Start import dashboard """
      auth_t = token.encode("ascii", "ignore")
      headers = {
          "Authorization": "Bearer " + token,
          "Content-type": "application/json",
      }
      url = 'http://{}:3000/api/dashboards/db'.format(grafana_ip)
      dashboard = {
         "dashboard": json.loads(self.dashboard_render(servers)),
         "overwrite": True
       }

      res = requests.post(url,headers=headers,json=dashboard)
      print("================================Import/update dashboard results:================================")
      print(res.text)
      print(res.status_code)
      return res.status_code

    def create_token(self,grafana_ip):
      
      '''Here we use the default org which is id 1'''
      grafana_url = 'http://admin:admin@{}:3000'.format(grafana_ip)
      grafana_url_org = grafana_url + '/api/user/using/1'
      grafana_url_api = grafana_url + '/api/auth/keys'
      grafana_key_name = "apikeycurl"
      grafana_key_role = "Admin"
      data = {"name":"apikeycurl", "role": "Admin"}
      r = requests.post(grafana_url_org)
      if r.text == '{"message":"Active organization changed"}':
        if len(json.loads(requests.get(grafana_url_api).text)) == 0:
          re = requests.post(grafana_url_api,json=data)
          key = json.loads(re.text)['key']
          return key
        elif (json.loads(requests.get(grafana_url_api).text)[0])['name'] == grafana_key_name:
          grafana_url_key_api = grafana_url_api + "/" + (json.loads(requests.get(grafana_url_api).text)[0])['id']
          re = requests.delete(grafana_url_key_api)
          '''Re-create api key'''
          res = requests.post(grafana_url_api,json=data)
          key = json.loads(re.text)['key']
          return key


class DictConvert(dict):
  def __str__(self):
    return json.dumps(self)
