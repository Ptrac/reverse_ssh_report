# reverse_ssh_report
Report the client connected to your SSH server


## Telegram

You'll need a Token and a Channel Id from Telegram.
There is plenty of tuto, ask google for that.

Once you have them, rename the credentials.json_example to credentials.json and update it with your credentials.


## Installation

poetry install

poetry run python main.py

chmod +x run.sh

## Crontab

Let's check for new client or disconnected one every 5 minutes.

crontab -e
```
*/5 * * * * /PATH/TO/YOUR/DIRECTORY/run.sh >> ~/cron.log 2>&1
```
