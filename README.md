# iCompute

## Setting Up the Testing Environment

1. In the repository setup the virtual environment:
```bash
python3 -m venv venv
```

2. Activate the environment.

On Unix like systems:

```bash
. venv/bin/activate
```

On Windows systems:

```cmd
venv\Scripts\activate.bat
```

3. Install the dependencies:

```bash
pip install -r requirements.txt 
```

## Running the Flask Application

First activate the environment see above.
Then launch flask.

On Unix like systems:

```bash
export FLASK_APP=logon
export FLASK_ENV=development
flask run
```

On Windows:

```cmd
set FLASK_APP=logon
set FLASK_ENV=development
flask run
```

Finally head over to [localhost:5000](http://127.0.0.1:5000) for testing!

