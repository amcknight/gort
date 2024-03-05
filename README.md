# Gort

A Twitch chatbot experiment for twitch.tv/mangort

## Install

Install git, python, pip, and gort using yum
```bash
sudo yum update -y
sudo yum -y install git python3 python3-pip
pip3 install pipenv
mkdir git
cd git
git clone https://github.com/amcknight/gort.git
cd gort
pipenv install
```

Set environment variables. I just create a file called `.env` in the `gort` folder.

Either fill them with sensitive keys directly:
```env
BOT_NICK=<BOT NAME>
CHANNEL=<TWITCH CHANNEL NAME>
TMI_TOKEN=<TMI TOKEN>
CLIENT_ID=<CLIENT ID>
OPENAI_API_KEY=<OPENAI API KEY>
```
Or point to those sensitive values in Amazon Secrets Manager and make sure your server is given an IAM Role to access them.
```env
BOT_NICK=<BOT NAME>
CHANNEL=<TWITCH CHANNEL NAME>
SECRETS_NAME=<AMAZON SECRETS NAME>
SECRETS_REGION=<AMAZON SECRETS REGION>
```

## Run

Go to the `gort` directory.

Run it manually with `pipenv run bot` or make it an auto-upgradable service with:
```bash
sudo cp gort.service /etc/systemd/system/
sudo systemctl enable gort
sudo systemctl start gort
```

The restarting the service will auto-upgrade with `git pull` before running `pipenv run bot`.
