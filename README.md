# flask_workout_API
This project is a backend REST API for a workout tracking application built with Flask, SQLAlchemy, and Marshmallow. It allows users to create workouts, define exercises, and associate them with workout sessions.

## Features
- Create, view, and delete workouts
- Create, view, and delete exercises
- Add exercises to specific workouts with sets/reps/duration
- Model, schema, and database-level validations
- Test suite using pytest

## Setup
export FLASK_APP=server/app.py
flask db init
flask db migrate -m "initial"
flask db upgrade

## Seed the DB
pipenv run python server/seed.py

## Run the App
pipenv run flask run --port=5555

## Run tests
pipenv run pytest
