from app.ai.llm_service import LLMService

class LLMProvider:
    @classmethod
    async def generate_explanation(cls, evidence_data):
        return await LLMService.generate_explanation(evidence_data)
