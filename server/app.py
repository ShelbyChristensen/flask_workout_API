from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema
from models import db, Workout, Exercise, WorkoutExercise


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()

###

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return workout_schema.dump(workout), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    try:
        workout_data = workout_schema.load(data)  # Deserialize + validate
        new_workout = Workout(**workout_data)
        db.session.add(new_workout)
        db.session.commit()
        return workout_schema.dump(new_workout), 201
    except Exception as e:
        return {"error": str(e)}, 400

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return '', 204



### Exercise Endpoints

@app.route('/exercises', methods=['GET'])
def get_exercises():
    return exercises_schema.dump(exercises), 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return exercise_schema.dump(exercise), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    try:
        exercise_data = exercise_schema.load(data)
        new_exercise = Exercise(**exercise_data)
        db.session.add(new_exercise)
        db.session.commit()
        return exercise_schema.dump(new_exercise), 201
    except Exception as e:
        return {"error": str(e)}, 400

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return '', 204


### Link the Exercise to the Workout

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    data = request.get_json()
    try:
        data['workout_id'] = workout_id
        data['exercise_id'] = exercise_id
        we_data = workout_exercise_schema.load(data)
        new_we = WorkoutExercise(**we_data)
        db.session.add(new_we)
        db.session.commit()
        return workout_exercise_schema.dump(new_we), 201
    except Exception as e:
        return {"error": str(e)}, 400

###

if __name__ == '__main__':
    app.run(port=5555, debug=True)
