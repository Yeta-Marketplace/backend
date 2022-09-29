"""
The default EmailStr in Pydantic does NOT lower 
the email part before the @ symbol

This was done on purpose accordint to:
https://github.com/pydantic/pydantic/issues/798

I don't like that. Therefore this custom type is created.
"""

from pydantic import EmailStr as PydanticEmailStr


class EmailStr(PydanticEmailStr):
    @classmethod
    def validate(cls, value: str) -> str:
        return super().validate(value).lower()
