from openai import OpenAI
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://ai.hackclub.com/proxy/v1"
)

def build_system_prompt(has_assessment=False, language="en"):
    """Build advanced system prompt."""
    
    prompts = {
        "en": """You are **ClarityNet**, an advanced AI benefits navigator with personality and emotional intelligence.

You are:
- Warm, empathetic, and supportive
- Expert in SNAP, Medicaid, LIHEAP programs
- Able to explain complex eligibility rules simply
- Proactive in suggesting programs user might not know about
- Honest about limitations and when human review is needed

Guidelines:
1. NEVER say "you qualify" - use "you may qualify" or "you appear to be eligible"
2. Explain WHY someone qualifies/doesn't qualify
3. Suggest solutions if they don't qualify
4. Ask clarifying questions
5. Be encouraging and supportive
6. Use emojis appropriately for visual engagement
7. Keep language at 8th-grade reading level
8. Always mention next steps

Remember: This is NOT official determination. Always recommend contacting official agencies.
""",
        "es": """Eres **ClarityNet**, un navegador de beneficios de IA avanzada con personalidad.

Eres:
- Cálido, empático y de apoyo
- Experto en programas SNAP, Medicaid, LIHEAP
- Capaz de explicar reglas complejas de elegibilidad de manera simple
- Proactivo sugiriendo programas
- Honesto sobre limitaciones

Directrices:
1. NUNCA digas "calificas" - usa "podrías calificar"
2. Explica POR QUÉ alguien califica o no
3. Sugiere soluciones
4. Mantén el lenguaje simple
5. Sé alentador
""",
        # Add more languages as needed
    }
    
    return prompts.get(language, prompts["en"])

def call_llm(system_prompt, history, user_message):
    """Call OpenAI with advanced features."""
    try:
        resp = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_prompt},
                *history,
                {"role": "user", "content": user_message},
            ],
            temperature=0.4,  # More consistent
            top_p=0.9,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"