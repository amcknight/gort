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

Set environment variables. I just create a file called `.env` in the `gort` folder with these filled in:
```env
TMI_TOKEN=<TMI TOKEN>
CLIENT_ID=<CLIENT ID>
BOT_NICK=<BOT NAME>
CHANNEL=<TWITCH CHANNEL NAME>
ENGINE=<OPENAI ENGINE>
OPENAI_API_KEY=<OPENAI API KEY>
AWS_ACCESS_KEY_ID=<AWS ACCESS KEY>
AWS_SECRET_ACCESS_KEY=<AWS SECRET KEY>
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
