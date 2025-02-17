# This script is used to display the connected clients on user request

import json
import os
import subprocess


def read_list(file):
    filename = os.path.join(file)
    try:
        with open(filename, mode="rb") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


connected_clients = []

cmd = "ss -ltupnr | grep localhost:"
result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
returned_output = result.stdout

for client in returned_output.decode("utf-8").splitlines():
    if "[::]:" in client.split()[5]:
        connected_clients.append(int(client.split()[4].split(":")[1]))

connected_clients.sort()

mapping = read_list("mapping.json")

mapping_dict = {client["ssh_port"]: client for client in mapping}

print("Connected clients:")
for client in connected_clients:
        if mapping:
            if client in mapping_dict:
                print(f"{client} - {mapping_dict[client]['device']}")
            else:
                print(f"{client} - Unknown in mapping")
        else:
            print(f"{client}")

