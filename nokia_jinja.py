from flask import Flask, render_template
from jinja2 import Template
import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
from netmiko.ssh_exception import  NetMikoTimeoutException

with open('conf_nokia.yaml') as f:
    config = yaml.load(f,Loader = yaml.FullLoader)

# load jinja2 template
env = Environment(loader = FileSystemLoader('C:\PATH\PATH\PATH\PATH'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template('template_nokia.j2')

# Render the template with data and print the output
rendered_data = template.render(config)
print(rendered_data)

ports = [21211, 21212, 21214, 21215, 21216]
# ports = [21215]

for port in ports:

    SR_SSH= {
        'device_type': 'device_type'
        'ip': 'X.X.X.X',
        'username': 'user',
        'password': 'pass',
        'port': port
    }

    net_connect = ConnectHandler(**SR_SSH)
    output = net_connect.send_command('show router interf')
    print (output)
    try:
        net_connect.send_config_set(rendered_data)  
    except (NetMikoTimeoutException):
        output2 = net_connect.send_command('show router interf')
        print (output2)
        continue 

#######################################

# conf_nokia.yaml

'''
interfaces:
  - interface: lo1
    desc: loopback-1
    ip_add: 10.0.1.1
    netmask: /32
    port: loopback 
  - interface: lo2
    desc: loopback-2 
    ip_add: 10.0.2.1
    netmask: /32
    port: loopback
  - interface: lo3
    desc: loopback-3-updated
    ip_add: 10.0.3.1
    netmask: /32
    port: loopback
'''

# template_nokia.j2

'''
{% for int in interfaces %}
/configure router interface {{ int.interface }}
address {{ int.ip_add }}{{ int.netmask }}
description {{ int.desc }}
{{ int.port }}
{% endfor %}
'''

#########################################
