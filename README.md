# Gort

A Twitch chatbot experiment for twitch.tv/mangort

## Install on EC2

### Configure and Launch an Instance

- Choose Amazon Linux 2023 AMI
- Select a Security Group that can TODO
- In Advanced Settings set the User Data to:
```bash
#!/bin/bash
yum update -y
yum -y install git python3 python3-pip
pip3 install pipenv
cd ~
mkdir git
cd git
git clone https://github.com/amcknight/gort.git
cd gort
pipenv install
cp gort.service /etc/systemd/system/
systemctl enable gort
systemctl start gort
```

- Launch the instance

### Set environment variables

I just create a file called `.env` in the `gort` folder with these filled in:

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

### Manually

Simply go into the `gort` directory and run `pipenv run bot`

### As an auto-upgradable service

In the `gort` directory:

```bash
sudo cp gort.service /etc/systemd/system/
sudo systemctl enable gort
sudo systemctl start gort
```

To upgrade, restart the service or server and it will `git pull` before running `pipenv run bot`.
