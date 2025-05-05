import json
import asyncio
from database.models import FAQ
from database.db import async_session


def prepare_data_faq():
    result_info = []
    with open('json_base/last_info_en.json', encoding='UTF-8') as file:
        result = json.load(file)

    for k, v in result.items():
        for a, b in v.items():
            result_info.append(FAQ(question=a, answer=b, category=k, lang='en'))
    return result_info


async def seed_faq():
    async with async_session() as session:


        faqs = prepare_data_faq()

        session.add_all(faqs)
        await session.commit()
        print("✅ FAQ-записи успешно добавлены.")


if __name__ == "__main__":
    asyncio.run(seed_faq())
