from src.config import *
from src.models import *


class CategoryService:
    def __init__(self, db):
        self.db = db

    def check_duplicate(self, ref, field, value):
        query = ref.where(field, ATTR_EQUAL, value)
        items = query.stream()
        return len(list(items)) > 0

    def get_category_doc_ref(self, id: str):
        return self.db.collection(FIREBASE_COLLECTION_CATEGORIES).document(id)

    def get_modified_category_json(self, id: str, category: str):
        return {PROMPT_ATTR_ID: id, PROMPT_ATTR_NAME: category}

    def create_category(self, category: Category):
        categories_ref = self.db.collection(FIREBASE_COLLECTION_CATEGORIES)
        if self.check_duplicate(categories_ref, PROMPT_ATTR_NAME, category.name):
            return None
        doc_ref = categories_ref.document()
        doc_ref.set(category.dict())
        return self.get_modified_category_json(doc_ref.id, category.name)

    def update_category(self, id: str, category: Category):
        categories_ref = self.db.collection(FIREBASE_COLLECTION_CATEGORIES)
        doc_ref = categories_ref.document(id)
        doc_ref.set(category.dict())
        return self.get_modified_category_json(id, category.name)

    def get_category(self, id: str):
        doc_ref = self.get_category_doc_ref(id)
        doc = doc_ref.get()
        return (
            self.get_modified_category_json(doc.id, doc.to_dict()[PROMPT_ATTR_NAME])
            if doc.exists
            else None
        )

    def get_all_categories(self):
        categories_ref = self.db.collection(FIREBASE_COLLECTION_CATEGORIES)
        categories = categories_ref.stream()
        category_list = [
            self.get_modified_category_json(
                category.id, category.to_dict()[PROMPT_ATTR_NAME]
            )
            for category in categories
        ]
        return category_list
