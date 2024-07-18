from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud, models, schemas
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new robot
@app.post("/robots/", response_model=schemas.Robot)
def create_robot(robot: schemas.RobotCreate, db: Session = Depends(get_db)):
    return crud.create_robot(db=db, robot=robot)


# Read robot by ID
@app.get("/robots/{robot_id}", response_model=schemas.Robot)
def read_robot(robot_id: int, db: Session = Depends(get_db)):
    db_robot = crud.get_robot(db, robot_id=robot_id)
    if db_robot is None:
        raise HTTPException(status_code=404, detail="Robot not found")
    return db_robot


# List all robot names
@app.get("/robots/main", response_model=List[schemas.RobotName])
def read_robots(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    robots = crud.get_robots(db, skip=skip, limit=limit)
    return [{"name": robot.name} for robot in robots]


@app.delete("/robots/{robot_name}", response_model=schemas.RobotName)
def delete_robot(robot_name: str, db: Session = Depends(get_db)):
    db_robot = crud.delete_robot_by_name(db, robot_name=robot_name)
    if db_robot is None:
        raise HTTPException(status_code=404, detail="Robot not found")
    return {"name": db_robot.name}


@app.put("/robots/speed", response_model=schemas.Robot)
def update_robot_speed(robot_update: schemas.RobotUpdateSpeed, db: Session = Depends(get_db)):
    db_robot = crud.update_robot_speed(db, robot_update=robot_update)
    if db_robot is None:
        raise HTTPException(status_code=404, detail="Robot not found")
    return db_robot


# Update robot camera by name
@app.put("/robots/camera", response_model=schemas.Robot)
def update_robot_camera(robot_update: schemas.RobotUpdateCamera, db: Session = Depends(get_db)):
    db_robot = crud.update_robot_camera(db, robot_update=robot_update)
    if db_robot is None:
        raise HTTPException(status_code=404, detail="Robot not found")
    return db_robot


@app.get("/get_robots")
def read_robots(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    robots = crud.get_robots(db, skip=skip, limit=limit)
    return robots


@app.get("/robot/{name}")
def read_robot(name: str, db: Session = Depends(get_db)):
    robot = crud.get_robot_by_id(db, name)
    if robot is None:
        raise HTTPException(status_code=404, detail="Robot not found")
    return robot
