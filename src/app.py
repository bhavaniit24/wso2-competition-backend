from src.firebase_service import FirebaseService
from src.ai_service import AIService
from src.models import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

# Initialize APP
app = FastAPI(
    title="bhavan-ai-api",
    version="0.0.1",
)

# Initialize Services
firebase_service = FirebaseService()
ai_service = AIService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return "Bhavan AI - API"


@app.get("/health")
def health():
    return {"status": "running"}


@app.get("/prompts/search")
def search_prompts(q: str = None, cid: str = None):
    return firebase_service.search_prompts(q, cid)


@app.get("/prompts/{prompt_id}")
def get_prompt(prompt_id: str):
    return firebase_service.get_prompt(prompt_id)


@app.post("/prompts")
def create_prompt(prompt: Prompt):
    return firebase_service.create_prompt(prompt)


@app.put("/prompts/{prompt_id}")
def update_prompt(prompt_id: str, prompt: Prompt):
    return firebase_service.update_prompt(prompt_id, prompt)


@app.delete("/prompts/{prompt_id}")
def delete_prompt(prompt_id: str):
    return firebase_service.delete_prompt(prompt_id)


@app.get("/categories/{category_id}")
def get_category(category_id: str):
    return firebase_service.get_category(category_id)


@app.get("/categories")
def get_all_categories():
    return firebase_service.get_all_categories()


@app.post("/categories")
def create_category(category: Category):
    return firebase_service.create_category(category)


@app.put("/categories/{category_id}")
def update_category(category_id: str, category: Category):
    return firebase_service.update_category(category_id, category)


@app.get("/prompts/category/{category_id}")
def get_prompts_by_category(category_id: str):
    return firebase_service.get_prompts_by_category(category_id)


@app.post("/apps")
def create_app(app: App):
    return firebase_service.create_app(app)


@app.post("/apps/use")
def create_app(app: UseApp):
    return firebase_service.use_app(app)


@app.put("/apps/{app_id}")
def update_app(app_id: str, app: App):
    return firebase_service.update_app(app_id, app)


@app.get("/apps/search")
def search_apps(q: str = None, cid: str = None):
    return firebase_service.search_apps(q, cid)


@app.post("/chat")
def chat(message: AIMessage):
    return ai_service.send_message(message.content)


@app.post("/chat/stream")
async def stream_chat(message: AIMessage):
    generator = ai_service.send_streaming_message(message.content)
    return StreamingResponse(generator, media_type="text/event-stream")


@app.post("/users")
def create_user(user: User):
    return firebase_service.create_user(user)


@app.post("/users/validate")
def create_user(user: ValidateUser):
    return firebase_service.validate_user(user)
