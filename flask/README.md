# Run Flask

    # bash
    export FLASK_APP=app.py
    python -m flask run
    # browse to 127.0.0.1:5000

    # bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    python -m flask run
    # browse to 127.0.0.1:5000

## SONGPRO_CHORUS_JSON env

Use this environment to customize the chorus db:

    export SONGPRO_CHORUS_JSON=chorus-25.json
    export FLASK_APP=app.py
    export FLASK_ENV=development
    python -m flask run
