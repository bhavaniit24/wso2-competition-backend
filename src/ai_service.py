import asyncio
from typing import AsyncIterable
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import AsyncIteratorCallbackHandler


class AIService:
    def __init__(self):
        self.callback = AsyncIteratorCallbackHandler()

    def get_chat_llm(self, stream=False):
        if stream:
            return ChatOpenAI(
                max_tokens=25,
                streaming=True,
                verbose=True,
                callbacks=[self.callback],
            )

        return ChatOpenAI(model="gpt-4")

    def send_custom_context_message(self, app_variable_list):
        template = ChatPromptTemplate.from_messages(app_variable_list)
        result = self.get_chat_llm()(template.format_messages())
        return result.content

    def send_message_prompt(self, message):
        template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                        You are an advanced helpful AI bot.
                        Your name is Bhavan AI.
                        You have access to previous chats and responses.
                        You also have access to updated real-time news and information.
                        Provide the response in markdown format.
                    """,
                ),
                ("human", "{user_input}"),
            ]
        )

        messages = template.format_messages(user_input=message)

        return messages

    def send_message(self, content: str) -> str:
        messages = self.send_message_prompt(content)
        result = self.get_chat_llm()(messages)
        return result.content

    async def send_streaming_message(self, content: str) -> AsyncIterable[str]:
        messages = self.send_message_prompt(content)

        task = asyncio.create_task(
            self.get_chat_llm(True).agenerate(messages=[messages])
        )

        try:
            async for token in self.callback.aiter():
                yield token
        except Exception as e:
            print(f"Caught exception: {e}")
        finally:
            self.callback.done.set()

        await task
