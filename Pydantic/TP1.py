from pydantic import BaseModel, EmailStr, field_validator

class User(BaseModel):
    name: str
    email: EmailStr
    account_id: int

    @field_validator("account_id")
    def validate_account_id(cls, value):
        if value <= 0:
            raise ValueError("account_id must be positive")
        return value


user1 = User(
    name="Ali",
    email="ali@gmail.com",
    account_id=123
)

print(user1)

try:
    user2 = User(
        name="Omar",
        email="omar",
        account_id=-5
    )
except Exception as e:
    print(e)


json_data = user1.model_dump_json()
print(json_data)

dict_data = user1.model_dump()
print(dict_data)