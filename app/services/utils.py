from urllib.parse import quote
import aiohttp
import asyncio
import json
from asgiref.sync import sync_to_async
from app.models import Translation

@sync_to_async
def get_translation(desc, lang_desc):
    try:
        return Translation.objects.get(text=desc, lang=lang_desc).result
    except Translation.DoesNotExist:
        return None

@sync_to_async
def save_translation(desc, lang_desc, result):
    Translation.objects.create(text=desc, lang=lang_desc, result=result)

async def trans_req(desc: str, lang_desc: str) -> str:
    if lang_desc == "en":
        return desc
    # Check database for existing translation
    db_result = await get_translation(desc, lang_desc)
    if db_result:
        return db_result

    # Encode the text for URL
    text = quote(desc)
    url = f"https://translate.googleapis.com/translate_a/single?sl=en&tl={lang_desc}&dt=t&q={text}&client=gtx"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                if response.status != 200:
                    return desc
                
                json_data = await response.json()
                
                if json_data and len(json_data) > 0 and len(json_data[0]) > 0 and len(json_data[0][0]) > 0:
                    translated_text = json_data[0][0][0]
                    if translated_text and translated_text != desc:
                        translated_text = translated_text.lower().capitalize()
                        # Save to database
                        await save_translation(desc, lang_desc, translated_text)
                        return translated_text
        return desc
    except (aiohttp.ClientError, asyncio.TimeoutError, json.JSONDecodeError, IndexError, TypeError):
        return desc

def sync_translate(text, lang_code):
    # Call the async function in a synchronous context
    return asyncio.run(trans_req(text, lang_code))

# print(trans_req('{"text":"Hello, how are you?"}', "es"))