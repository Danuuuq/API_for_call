from pydantic import BaseModel


class Calling(BaseModel):
    caller: int
    name_caller: str
    called: int


class ResultCall(BaseModel):
    result: str
