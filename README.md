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

```bash
flask run
```

Finally head over to [localhost:5000](http://127.0.0.1:5000) for testing!

## Adding Test Data

First access environment set up above. 
Then use flask command.

```bash
flask add-testing-data
```
