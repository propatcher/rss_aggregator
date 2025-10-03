from pydantic import BaseModel, ConfigDict, field_validator,EmailStr

class SUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    login: str
    email: EmailStr

class SUserRegistration(BaseModel):
    login: str
    email: EmailStr
    password: str
    
    @field_validator('login')
    def validate_login(cls, v:str):
        v = v.strip()
        if len(v) < 3:
            raise ValueError('Логин слишком короткий')
        return v
    @field_validator('password')
    def validate_password(cls, v:str):
        if len(v) < 8:
            raise ValueError('Пароль не может быть меньше 8 символов')
        if v.isalpha():
            raise ValueError("Пароль должен состоять не только из алфавитных букв")
        if v.isdigit():
            raise ValueError("Пароль не может содержать только цифры")
        return v
        
class SUserLogin(BaseModel):
    identifier: str
    password: str
    
    @field_validator('identifier')
    def validate_identifier(cls,v:str):
        v = v.strip()
        if not v:
            raise ValueError('Identifier cannot be empty')
        if '@' in v and '.' in v:
            try:
                EmailStr._validate(v)
            except ValueError:
                raise ValueError("Invalid email format")
        return v
    