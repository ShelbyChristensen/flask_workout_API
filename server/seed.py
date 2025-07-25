#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():
    print("Starting")
    db.drop_all()
    db.create_all()

    print("Creating exercises...")
    pushups = Exercise(name="Push Ups", category="Strength", equipment_needed=False)
    squats = Exercise(name="Squats", category="Strength", equipment_needed=False)
    jumping_jacks = Exercise(name="Jumping Jacks", category="Cardio", equipment_needed=False)

    print("Creating workouts...")
    workout1 = Workout(date=date(2025, 7, 1), duration_minutes=30, notes="Morning strength workout")
    workout2 = Workout(date=date(2025, 7, 2), duration_minutes=20, notes="Cardio burst")

    print("Saving exercises and workouts...")
    db.session.add_all([pushups, squats, jumping_jacks, workout1, workout2])
    db.session.commit()

    print("Adding exercises to workouts...")
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=pushups.id, reps=15, sets=3)
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=squats.id, reps=20, sets=4)
    we3 = WorkoutExercise(workout_id=workout2.id, exercise_id=jumping_jacks.id, duration_seconds=120)

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Complete.")
