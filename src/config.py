import os


FIREBASE_COLLECTION_PROMPTS: str = "prompts"
FIREBASE_COLLECTION_CATEGORIES: str = "categories"
FIREBASE_COLLECTION_APPS: str = "apps"
FIREBASE_SUB_COLLECTION_MESSAGES: str = "messages"

ATTR_EQUAL: str = "=="
ATTR_GTE: str = ">="
ATTR_LTE: str = "<="
ATTR_ARRAY_CONTAINS: str = "array_contains"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FIREBASE_PATH = os.getenv("FIREBASE_PATH")
