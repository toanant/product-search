## Dependencies

- Python 2.7
- python-lxml
- python-pyquery
- python-celery
- rabbitmq-server
- elasticsearch
- pyelasticsearch
- python-flask
- python-requests
- python-pymongo
- mongodb-server

## Steps

### Install dependencies
# sudo aptitude build-dep python-lxml python-pyquery python-celery python-requests python-pymongo

### Install python-pip

 sudo aptitude install python-pip python-virtualenv

### create virtualenv

virtualenv --distribute venv

### Activate virtualenv

source venv/bin/activate

### instal python-packages using pip

# pip install pyquery Celery Flask requests pymongo -U
sudo pip install -U https://github.com/rhec/pyelasticsearch/archive/0.2.zip


sudo aptitude install mongodb-server rabbitmq-server
