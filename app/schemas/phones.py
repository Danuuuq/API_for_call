from pydantic import BaseModel, Field


class PhoneBase(BaseModel):
    phone_number: int
    display_name: str
    last_ip: str
    # mac_address: str

class PhoneUpdateBase(BaseModel):
    phone_number: int
    last_ip: str
