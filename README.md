# Real-Time Chat App - CS50x 2023 Final Project
#### Video Demo: TODO
#### Description:

## Overview

> ### Real-Time Chat App
> ### Flask + SocketIO project

## Content

1. [Routing](#routing)
2. [Application Structure](#application-structure)
3. [Run locally](#run-locally)
4. [Port](#port)
5. [Sources](#sources)
6. [License](#license)


## Routing

- Home page (URL: /)
  - This page contains a search form. The search form returns a list of users with 'Send message' button.
- Chat page (URL: /chat/<resource_id>)
  - This page contains the real-time chat.

## Aplication Structure

- `static/` - This folder contains the js, css files and the favicon.
- `templates/` - This folder contains the html templates.
- `__init__.py`- This file contains the create_app function for the application setup.
- `auth.py` - This file contains the auth related routes.
- `chat.py` - This file contains the chat related routes.
- `db.py` - This file contains the functions for the db setup.
- `events.py` - This file contains the socketio related functions.
- `extensions.py` - This file contains socketio instance.
- `query_texts.py` - This file contains query texts.
- `schema.sql` - This file contains the schema of the database.
- `instances/` - This folder contains the sqlite database.
- `.env` - This file contains the environment variables. e.g.: SECRET_KEY
- `.gitignore` - This file contains the files that are not part of the git repository.
- `LICENSE` - This file contains the license informations.
- `requirements.txt` - This file contains the necessary dependencies.


## Run locally

You need have Python 3.10.12 or higher.

### Preparation:

- I used Ubuntu WSL for the development
- clone the project
- create .env file and SECRET_KEY=<SECRET_KEY>

### Run
```sh
  # Ubuntu WSL
  sudo apt update && sudo apt upgrade
  sudo apt upgrade python3
  sudo apt install python3-pip
  sudo apt install python3-venv

  # create venv
  python3 -m venv .venv

  # Activate the venv
  source .venv/bin/activate

  # install dependencies
  pip install -r requirement.txt

  # init database
  flask --app flaskr init-db 

  # run in locally
  flask --app flaskr run --debug

  # Deactivate venv, if you close the project
  deactivate
```

## Port

The project uses 5000.

## Sources
- I've used the Flask framework and its official documentation as a reference for this project.
https://flask.palletsprojects.com/en/3.0.x/
- I've used Bootstrap for styling this project.
https://getbootstrap.com/
- I've use for favicon:
https://favicon.io/favicon-converter/
- I've learned from this video for this project.
https://www.youtube.com/watch?v=AMp6hlA8xKA

## License

MIT
