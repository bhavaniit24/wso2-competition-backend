import enum
from pydantic import BaseModel

PROMPT_ATTR_TEXT: str = "text"
PROMPT_ATTR_CATEGORY: str = "category"
PROMPT_ATTR_STATUS: str = "status"
PROMPT_ATTR_NAME: str = "name"
PROMPT_ATTR_ID: str = "id"
PROMPT_ATTR_CATEGORIES: str = "categories"
PROMPT_ATTR_DESCRIPTION: str = "description"
PROMPT_ATTR_ICON: str = "icon"
PROMPT_ATTR_MESSAGES: str = "messages"


class Prompt(BaseModel):
    text: str
    status: str
    categories: list[str]


class Category(BaseModel):
    name: str


class Variable(BaseModel):
    id: str
    content: str
    type: str


class Message(BaseModel):
    role: str
    content: str
    type: str
    variables: list[Variable]


class App(BaseModel):
    name: str
    description: str
    icon: str
    categories: list[str]
    messages: list[Message]


class AIMessage(BaseModel):
    content: str
    model: str


class UseVariable(BaseModel):
    id: str
    content: str


class UseApp(BaseModel):
    app_id: str
    variables: list[UseVariable]


class Status(str, enum.Enum):
    CREATED = "CREATED"
    DELETED = "DELETED"


class User(BaseModel):
    email: str
    email_verified: bool
    password: str
    display_name: str
    photo_url: str
    disabled: bool


class ValidateUser(BaseModel):
    email: str
    password: str
