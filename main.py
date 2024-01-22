import json
import os
import subprocess

import telepot


def get_credentials() -> dict:
    filename = os.path.join("credentials.json")
    try:
        with open(filename, mode="r") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}


def read_list(file):
    filename = os.path.join(file)
    try:
        with open(filename, mode="rb") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def write_list(a_list):
    with open("clients.json", "w") as f:
        json.dump(a_list, f)


credentials = get_credentials()


# Telegram
bot_token = credentials["BOT_TOKEN"]
bot_chatID = credentials["BOT_CHATID"]
bot = telepot.Bot(bot_token)

current_clients = []

cmd = "ss -ltupnr | grep ip6-localhost:"
returned_output = subprocess.check_output(cmd, shell=True)


for client in returned_output.decode("utf-8").splitlines():
    current_clients.append(int(client.split()[4].split(":")[1]))


previous_clients = read_list("clients.json")
mapping = read_list("mapping.json")

mapping_dict = {client["ssh_port"]: client for client in mapping}

for client in current_clients:
    if client not in previous_clients:
        if mapping:
            if client in mapping_dict:
                bot.sendMessage(
                    bot_chatID, f"{mapping_dict[client]['device']} ({client}) connected"
                )
            else:
                bot.sendMessage(bot_chatID, f"UNKNOWN Client : {client} connected")
        else:
            bot.sendMessage(bot_chatID, f"{client} connected")


for client in previous_clients:
    if client not in current_clients:
        if mapping:
            if client in mapping_dict:
                bot.sendMessage(
                    bot_chatID, f"{mapping_dict[client]['device']} ({client}) disconnected"
                )
            else:
                bot.sendMessage(bot_chatID, f"UNKNOWN Client : {client} disconnected")
        else:
            bot.sendMessage(bot_chatID, f"{client} disconnected")

write_list(current_clients)
