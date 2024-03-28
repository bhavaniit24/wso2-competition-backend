from src.config import *
from src.models import *


class PromptService:
    def __init__(self, db):
        self.db = db

    def check_duplicate(self, ref, field, value):
        query = ref.where(field, ATTR_EQUAL, value)
        items = query.stream()
        return len(list(items)) > 0

    def get_modified_prompt_json(self, id: str, prompt: str, status=Status.CREATED):
        return {
            PROMPT_ATTR_ID: id,
            PROMPT_ATTR_TEXT: prompt,
            PROMPT_ATTR_STATUS: status,
        }

    def get_prompt_doc_ref(self, id: str):
        return self.db.collection(FIREBASE_COLLECTION_PROMPTS).document(id)

    def get_category_doc_ref(self, id: str):
        return self.db.collection(FIREBASE_COLLECTION_CATEGORIES).document(id)

    def get_prompt(self, id):
        doc_ref = self.get_prompt_doc_ref(id)
        doc = doc_ref.get()
        return (
            self.get_modified_prompt_json(doc.id, doc.to_dict()[PROMPT_ATTR_TEXT])
            if doc.exists
            else None
        )

    def search_prompts(self, query=None, category=None):
        prompts_list = []
        prompts_ref = self.db.collection(FIREBASE_COLLECTION_PROMPTS)

        if category:
            category_ref = self.get_category_doc_ref(category)
            prompts_ref = prompts_ref.where(
                PROMPT_ATTR_CATEGORIES, ATTR_ARRAY_CONTAINS, category_ref
            )

        prompts = prompts_ref.stream()

        for prompt in prompts:
            data = prompt.to_dict()
            category_refs = data[PROMPT_ATTR_CATEGORIES]
            category_names = [
                category_ref.get().to_dict()[PROMPT_ATTR_NAME]
                for category_ref in category_refs
            ]

            prompts_list.append(
                {
                    PROMPT_ATTR_ID: prompt.id,
                    PROMPT_ATTR_TEXT: data[PROMPT_ATTR_TEXT],
                    PROMPT_ATTR_STATUS: data[PROMPT_ATTR_STATUS],
                    PROMPT_ATTR_CATEGORIES: [
                        {
                            PROMPT_ATTR_ID: category_ref.id,
                            PROMPT_ATTR_NAME: category_name,
                        }
                        for category_ref, category_name in zip(
                            category_refs, category_names
                        )
                    ],
                }
            )

        if query:
            new_prompts_list = [
                prompt
                for prompt in prompts_list
                if query.lower() in prompt[PROMPT_ATTR_TEXT].lower()
            ]

            return new_prompts_list

        return prompts_list

    def get_prompts_by_category(self, category):
        prompts_ref = self.db.collection(FIREBASE_COLLECTION_PROMPTS)
        category_ref = self.get_category_doc_ref(category)
        query = prompts_ref.where(
            PROMPT_ATTR_CATEGORIES, ATTR_ARRAY_CONTAINS, category_ref
        )
        prompts = query.stream()
        prompt_list = [
            self.get_modified_prompt_json(prompt.id, prompt.to_dict()[PROMPT_ATTR_TEXT])
            for prompt in prompts
        ]
        return prompt_list

    def create_prompt(self, prompt: Prompt):
        prompts_ref = self.db.collection(FIREBASE_COLLECTION_PROMPTS)
        category_refs = [
            self.get_category_doc_ref(category) for category in prompt.categories
        ]

        for category_ref in category_refs:
            if not category_ref.get().exists:
                print(f"The category '{category_ref.id}' does not exist.")
                return None

        if self.check_duplicate(prompts_ref, PROMPT_ATTR_TEXT, prompt.text):
            print(f"The prompt is duplicated.")
            return None

        data = {
            PROMPT_ATTR_TEXT: prompt.text.strip(),
            PROMPT_ATTR_STATUS: prompt.status,
            PROMPT_ATTR_CATEGORIES: category_refs,
        }

        doc_ref = prompts_ref.document()
        doc_ref.set(data)
        return self.get_modified_prompt_json(doc_ref.id, prompt.text)

    def update_prompt(self, prompt_id, new_prompt_data: Prompt):
        prompts_ref = self.db.collection(FIREBASE_COLLECTION_PROMPTS)

        prompt_ref = prompts_ref.document(prompt_id)

        if not prompt_ref.get().exists:
            print(f"The prompt with ID '{prompt_id}' does not exist.")
            return None

        category_refs = [
            self.get_category_doc_ref(category)
            for category in new_prompt_data.categories
        ]

        for category_ref in category_refs:
            if not category_ref.get().exists:
                print(f"The category '{category_ref.id}' does not exist.")
                return None

        data = {
            PROMPT_ATTR_TEXT: new_prompt_data.text,
            PROMPT_ATTR_STATUS: new_prompt_data.status,
            PROMPT_ATTR_CATEGORIES: category_refs,
        }

        prompt_ref.update(data)
        return self.get_modified_prompt_json(prompt_id, new_prompt_data.text)

    def delete_prompt(self, id):
        doc_ref = self.get_prompt_doc_ref(id)
        doc = doc_ref.get()
        doc_ref.delete()
        return (
            self.get_modified_prompt_json(
                doc.id, doc.to_dict()[PROMPT_ATTR_TEXT], Status.DELETED
            )
            if doc.exists
            else None
        )
