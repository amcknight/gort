# Gort

A Twitch chatbot experiment for https://www.twitch.tv/mangort

## Install

Install git, python, pip, and gort using yum
```bash
sudo dnf update -y
sudo dnf -y install git python python-pip
pip install pipenv
mkdir git
cd git
git clone https://github.com/amcknight/gort.git
cd gort
pipenv install
```

Set environment variables. I just create a file called `.env` in the `gort` folder.

Either fill them with sensitive keys directly:
```env
TMI_TOKEN=<TMI TOKEN> # Got from (https://twitchapps.com/tmi)
CLIENT_ID=<CLIENT ID> # Got from (https://dev.twitch.tv/console/apps) after registering the app
OPENAI_API_KEY=<OPENAI API KEY>
ANTHROPIC_API_KEY=<ANTHROPIC API KEY>
BOT_NICK=<BOT NAME>
CHANNEL=<TWITCH CHANNEL NAME>
COMPLETER=gpt3.5
```
Or point to those sensitive values in Amazon Secrets Manager and make sure your server is given an IAM Role to access them.
```env
SECRETS_NAME=<AMAZON SECRETS NAME>
SECRETS_REGION=<AMAZON SECRETS REGION>
BOT_NICK=<BOT NAME>
CHANNEL=<TWITCH CHANNEL NAME>
COMPLETER=gpt3.5
```

## Run

Go to the `gort` directory.

Run it manually with `pipenv run bot` or make it an auto-upgradable service with:
```bash
sudo cp gort.service /etc/systemd/system/
sudo systemctl enable gort
sudo systemctl start gort
```

Restarting the service will auto-upgrade with `git pull` before running `pipenv run bot`.
