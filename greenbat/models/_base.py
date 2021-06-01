import pydantic


class Model(pydantic.BaseModel):
    pass


class ORMModel(Model):
    class Config(pydantic.BaseConfig):
        orm_mode = True
