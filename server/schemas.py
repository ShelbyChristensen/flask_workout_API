from marshmallow import Schema, fields, validates, ValidationError
from models import Workout, Exercise, WorkoutExercise

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)

    @validates('name')
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Exercise name cannot be blank.")
        if len(value.strip()) < 3:
            raise ValidationError("Exercise name must be at least 3 characters long.")

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str()
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True)

    @validates('duration_minutes')
    def validate_duration(self, value):
        if value <= 0:
            raise ValidationError("Workout duration must be greater than 0 minutes.")