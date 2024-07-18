from pydantic import BaseModel


class RobotBase(BaseModel):
    name: str


class RobotCreate(RobotBase):
    pass


class Robot(RobotBase):
    id: int
    camera: str
    wheels: bool
    battery: int
    speed: int

    class Config:
        orm_mode = True


class RobotName(BaseModel):
    name: str

    class Config:
        orm_mode = True


class RobotUpdateSpeed(BaseModel):
    name: str
    speed: int


class RobotUpdateCamera(BaseModel):
    name: str
    camera: str
