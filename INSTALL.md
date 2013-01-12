## Dependencies

- Python 2.7
- rabbitmq-server
- elasticsearch
- mongodb-server

## Steps

### Install python-pip

 sudo aptitude install python-pip python-virtualenv

### Create virtualenv

virtualenv --distribute venv

### Activate virtualenv

source venv/bin/activate

### instal python-packages using pip

 pip install -r requirements.txt

### Install `mongodb-server`, `rabbitmq-server`
 sudo aptitude install mongodb-server rabbitmq-server

###
 Download and install latest stable release of `elasticsearch` from [official website](http://www.elasticsearch.org/download/)
