# app/ai/gemini_client.py

import os
import httpx

# Try to load SDK (optional)
USE_SDK = False
try:
    import google.generativeai as genai
    USE_SDK = True
except:
    USE_SDK = False

# ----------------------------------------
# Environment variables
# ----------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

if USE_SDK:
    genai.configure(api_key=GEMINI_API_KEY)


# ----------------------------------------
# SDK-based call (First preference)
# ----------------------------------------
def sdk_generate(prompt: str, max_output_tokens: int = 700) -> str:
    model = genai.GenerativeModel(GEMINI_MODEL)

    response = model.generate_content(
        prompt,
        generation_config={"max_output_tokens": max_output_tokens}
    )

    # New Gemini SDK returns text inside `.text`
    if hasattr(response, "text"):
        return response.text

    # Backup access
    try:
        return response.candidates[0].content.parts[0].text
    except:
        return str(response)


# ----------------------------------------
# HTTP fallback (always works)
# ----------------------------------------
async def http_generate(prompt: str, max_output_tokens: int = 700) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_output_tokens}
    }

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, params={"key": GEMINI_API_KEY}, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return str(data)


# ----------------------------------------
# Public unified function
# ----------------------------------------
async def call_gemini(prompt: str, max_output_tokens: int = 700) -> str:

    # Try SDK first
    if USE_SDK:
        try:
            return sdk_generate(prompt, max_output_tokens)
        except Exception as e:
            print("⚠️ Gemini SDK failed, switching to HTTP:", e)

    # Fallback always works
    return await http_generate(prompt, max_output_tokens)
