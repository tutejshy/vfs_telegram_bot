## VFS Telegram Bot

### Roadmap
- Docker
  - docker-compose
- Python >= 3.8
- sqlite
- sqlalchemy
- pydantic
- python-dotenv
- cloudscraper
  - requests
- apscheduler
  - pytz
- dependency-injector
- python-telegram-bot


### Dependencies
```console  
- pydantic
- python-dotenv

- requests        
- cloudscraper     
- sqlalchemy

- python-telegram-bot
- apscheduler
- pytz

- dependency-injector
```
### Installation
All variables must be registered in the **.env** file
```console
DEBUG=<True/False>
TOKEN=<TELEGRAM TOKEN>

CHAT_ID=<TELEGRAM CHAT ID>
DEV_CHAT_ID=<TELEGRAM DEV CHAT ID>

BOT_LOGIN=admin
BOT_PASSWORD=admin

DATABASE_URI=sqlite:///tracker.db

LOGINS_ENCODED=<csv file encoded in base64>
```
### Manual start
>if pycharm is used, these steps can be skipped

1. Create a virtual environment
```console
$python -m venv venv
```
2. Activate the virtual environment 
```console
$source venv/bin/activate
```
3. Install dependencies
```console
(venv)$pip install -r requirements.txt
```
4. Run a project
```console
(venv)$PYTHONPATH=$(pwd) python app/main.py
```
### Run it
```console
$docker-compose up --build -d  # build, d - optional params
```
### Run tests
Work In Progress
### Skeleton
```console  
app
    ├── core            -
    ├── db              -
    ├── di              -
    ├── models          -
    │   ├── domain      -        
    │   └── schemas     -
    ├── repo            -
    │   └── dao         -
    ├── services        -
    │   ├── bot         -    
    │   └── machines    -
    ├── util            -
    └── main.py         -     
```
### References
* [docker](https://www.docker.com/)
* [python](https://www.python.org/)
* [sqlite](https://sqlite.org/index.html)
* [sqlalchemy](https://www.sqlalchemy.org/)
* [pydantic](https://pydantic-docs.helpmanual.io/)
* [python-dotenv](https://github.com/theskumar/python-dotenv)
* [requests](https://docs.python-requests.org/en/latest/)
* [cloudscraper](https://github.com/venomous/cloudscraper)
* [apscheduler](https://github.com/agronholm/apscheduler)
* [pytz](https://pypi.org/project/pytz/)
* [dependency-injector](https://python-dependency-injector.ets-labs.org/)
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
