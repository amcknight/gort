# Gort

A Twitch chatbot experiment for twitch.tv/mangort

## Install

You need Python3.10, pipenv, and git. Detailed instructions below are for EC2.

`sudo yum update -y`

### Python 3.10

 Python installation instructions below are taken from [here](https://www.gcptutorials.com/post/python-3.10-installation-on-amazon-linux-2)

```bash
cd ~
sudo yum -y groupinstall "Development Tools"
sudo yum -y install gcc devel libffi-devel openssl11 openssl11-devel
wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz
tar zxvf Python-3.10.4.tgz
rm Python-3.10.4.tgz
cd Python-3.10.4
./configure --enable-optimizations
make
sudo make altinstall
cd ..
```

### Git

```bash
cd ~
mkdir git
cd git
git clone https://github.com/amcknight/gort.git
cd gort
```

### Pipenv

```bash
pip3 install pipenv
pipenv install
```

### Set environment variables

Set these environment variables. I recommend just creating a file called `.env` and putting it in the `gortbot` folder with these filled in.

```env
TMI_TOKEN=<TMI TOKEN>
CLIENT_ID=<CLIENT ID>
BOT_NICK=<BOT NAME>
CHANNEL=<TWITCH CHANNEL NAME>
OPENAI_API_KEY=<OPENAI API KEY>
```

## Running Gort

### Manually

Simply go into the `gort` directory and run `pipenv run bot`

### As an auto-upgradable service

In the `gort` directory:

```bash
sudo cp gort.service /etc/systemd/system/
sudo systemctl start gort
sudo systemctl enable gort
```

To upgrade, restart the service or server and it will `git pull` before running `pipenv run bot`.
