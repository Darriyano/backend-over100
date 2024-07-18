from fastapi import HTTPException

from sqlalchemy.orm import Session
import models, schemas
import random


def get_robot(db: Session, robot_id: int):
    return db.query(models.Robot).filter(models.Robot.id == robot_id).first()


def get_robots(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Robot).offset(skip).limit(limit).all()


def create_robot(db: Session, robot: schemas.RobotCreate):
    # Check if the robot name already exists
    existing_robot = db.query(models.Robot).filter(models.Robot.name == robot.name).first()
    if existing_robot:
        raise HTTPException(status_code=409, detail="Robot with the same name already exists")

    # If the robot name doesn't exist, create a new robot
    db_robot = models.Robot(
        name=robot.name,
        camera=random.choice(["port1", "port2", "port3"]),
        wheels=random.choice([True, False]),
        battery=random.randint(1, 100),
        speed=random.randint(1, 100)
    )
    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)
    return db_robot


def delete_robot_by_name(db: Session, robot_name: str):
    db_robot = db.query(models.Robot).filter(models.Robot.name == robot_name).first()
    if db_robot:
        db.delete(db_robot)
        db.commit()
        return db_robot
    return None


def update_robot_speed(db: Session, robot_update: schemas.RobotUpdateSpeed):
    db_robot = db.query(models.Robot).filter(models.Robot.name == robot_update.name).first()
    if db_robot:
        db_robot.speed = robot_update.speed
        db.commit()
        db.refresh(db_robot)
        return db_robot
    return None


def update_robot_camera(db: Session, robot_update: schemas.RobotUpdateCamera):
    db_robot = db.query(models.Robot).filter(models.Robot.name == robot_update.name).first()
    if db_robot:
        db_robot.camera = robot_update.camera
        db.commit()
        db.refresh(db_robot)
        return db_robot
    return None


def get_robot_by_id(db: Session, robot_id: str):
    return db.query(models.Robot).filter(models.Robot.name == robot_id).first()
