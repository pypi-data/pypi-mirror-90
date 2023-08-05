import requests
from ruamel import yaml

# TODO: change this branch to master when gateway stuff is merged
r = requests.get(
    "https://raw.githubusercontent.com/RhodiumGroup/helm-chart/gateway-tweaks/values.yml"
)

data = yaml.safe_load(r.content)["dask-gateway"]["gateway"]["extraConfig"][
    "optionHandler"
]

# change float cores to int cores b/c float not allowed for local cluster

data = "from math import ceil\nfrom dask_gateway_server.options import Integer\n" + data
data = data.replace('Float("cpus"', 'Integer("cpus"').replace(
    'Float("scheduler_cores", default=3.5', 'Integer("scheduler_cores", default=1'
)

with open("dask_gateway_config.py", "w") as f:
    f.write(data)
