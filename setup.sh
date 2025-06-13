#!/bin/sh
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt -y full-upgrade
sudo apt -y install python3.10 python3.10-venv python3.10-dev
sudo apt -y install python3-pip
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 2
cd /opt/mindary-python
mkdir logs
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py FLASK_ENV=development FLASK_DEBUG=1
nohup flask run --host=0.0.0.0 > logs/audit.log &
#python app.py