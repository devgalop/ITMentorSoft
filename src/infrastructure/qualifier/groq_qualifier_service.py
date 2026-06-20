import uuid

from dotenv import load_dotenv
import os
from groq import Groq
import json
import asyncio
from src.features.assessments.shared.qualifier_service import (
    QualifierPrompt,
    QualifierResult,
    QualifierService,
)

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")


class GroqQualifierService(QualifierService):

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.generic_prompt: str = self.get_generic_prompt()

    async def qualify(self, qualifier_prompt: QualifierPrompt) -> QualifierResult:

        completion = await asyncio.to_thread(
            self.client.chat.completions.create,
            model="qwen/qwen3-32b",
            messages=[
                {"role": "system", "content": self.get_prompt(qualifier_prompt)},
                {"role": "user", "content": qualifier_prompt.user_answer},
            ],
            temperature=0.6,
            max_completion_tokens=4096,
            top_p=0.95,
            reasoning_effort="default",
            stream=False,
            stop=None,
        )

        response = completion.choices[0].message.content
        if not response:
            raise ValueError("Received empty response from the qualifier service.")

        if "</think>" in response:
            response = response.split("</think>")[1].strip()

        if not response.startswith("{") and not response.endswith("}"):
            raise ValueError(f"Received response is not a valid JSON: {response}")

        response_json = json.loads(response)

        return QualifierResult(
            id=uuid.uuid4().hex,
            question_id=qualifier_prompt.rubric.question_id,
            user_id=qualifier_prompt.user_id,
            score=response_json.get("score", 0),
            feedback=response_json.get("feedback", ""),
            key_concepts_detected=response_json.get("key_concepts_detected", []),
            misconceptions_detected=response_json.get("misconceptions_detected", []),
            question_topic=qualifier_prompt.rubric.classification,
            assessment_id=qualifier_prompt.assessment_id,
            question_difficulty=qualifier_prompt.rubric.difficulty.value,
            answer_id=qualifier_prompt.answer_id,
        )

    def get_prompt(self, qualifier_prompt: QualifierPrompt) -> str:
        """Generates the prompt for the qualifier service by replacing placeholders in the generic prompt.

        Args:
            qualifier_prompt (QualifierPrompt): The qualifier prompt containing the rubric and qualifier mode.

        Returns:
            str: The generated prompt with placeholders replaced by actual values.
        """
        rubric_to_text = qualifier_prompt.rubric.to_text()
        prompt = self.generic_prompt.replace("%RUBRICA%", rubric_to_text).replace(
            "%MODO_CALIFICACION%", qualifier_prompt.qualifier_mode
        )
        return prompt

    def get_generic_prompt(self) -> str:
        """Reads the generic prompt from a text file and returns it as a string.

        Returns:
            str: The base prompt to be used for the qualifier service, with placeholders for the rubric and qualifier mode.
        """
        prompt_file = os.path.join(os.path.dirname(__file__), "input_prompt.txt")
        with open(prompt_file, "r", encoding="utf-8") as f:
            return f.read()
