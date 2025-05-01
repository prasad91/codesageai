import os

USE_OFFLINE_MOCK = True  # ← Toggle this to False when using real OpenAI

def get_refactor_suggestion(code_block: str) -> str:
    if USE_OFFLINE_MOCK:
        # Return a fake "refactored" version for testing
        return f"// [MOCKED] Refactored version of:\n{code_block.strip()}"
    
    # Real OpenAI API (if quota restored)
    import openai
    openai.api_key = os.getenv("OPENAI_TOKEN")

    prompt = f"""You are a senior Java developer. Improve the following method for readability, error handling, and best practices:\n\n{code_block}"""

    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful backend code refactoring assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=800
    )

    return response["choices"][0]["message"]["content"].strip()
