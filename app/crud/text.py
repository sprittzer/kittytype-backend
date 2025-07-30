from typing import Optional
from app.models.text import Text


async def create_text(
    body: str,
    language: str = "en",
    mode: str = "time",
    length: Optional[int] = None,
    punctuation: bool = False,
    numbers: bool = False,
) -> Text:
    text = await Text(
        body=body,
        language=language,
        mode=mode,
        length=length,
        punctuation=punctuation,
        numbers=numbers,
    )
    return text


async def get_text_by_id(text_id: int) -> Optional[Text]:
    return await Text.get_or_none(id=text_id)

async def get_random_text_advanced(
    mode: str,
    language: str = "en",
    punctuation: Optional[bool] = None,
    numbers: Optional[bool] = None,
    length: Optional[int] = None
) -> Optional[Text]:
    query = Text.filter(mode=mode, language=language)
    
    if punctuation is not None:
        query = query.filter(punctuation=punctuation)
    if numbers is not None:
        query = query.filter(numbers=numbers)
    if length is not None:
        query = query.filter(length=length)
    
    return await query.order_by_rand().first()


async def delete_text(text_id: int) -> bool:
    text = await Text.get_or_none(id=text_id)
    await text.delete()
    if text: return True
    return False