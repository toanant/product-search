#Description
To be updated

#Getting Started
1. Read `Install.md` for installation instructions.
2. Once instllation has been completed, type following commands

```bash
## `cd` to `utils/`
cd utils/
## Run celery worker under screen session
screen -dmS "celery" celery -A tasks worker --loglevel=info --concurrency=4
## Run crawler using
python crawl.py
```
