import json


def get_keys_of_service(name):
    if name == 'Вклады':
        file_name = 'deposit'
    elif name == 'Кредиты':
        file_name = 'detailed_loan_info'
    elif name == 'Карты':
        file_name = 'cards_result'
    else:
        file_name = None
    with open(f'services_json/{file_name}.json', mode='r', encoding='UTF-8') as file:
        content = json.load(file)
        names = list(content.keys())
    return names


def get_info_of_service(name):
    if name == 'Вклады':
        file_name = 'deposit'
    elif name == 'Кредиты':
        file_name = 'detailed_loan_info'
    elif name == 'Карты':
        file_name = 'cards_result'
    else:
        file_name = None
    with open(f'services_json/{file_name}.json', mode='r', encoding='UTF-8') as file:
        content = json.load(file)
    return content

def deposit_info(category, idx):
    product_name = get_keys_of_service(category)[int(idx)]
    content = get_info_of_service(category)
    info = content[product_name]
    description = info['description']
    detail_link = info['detail_link']
    image = info['image']
    return [product_name, description, detail_link, image]


def get_about_info(lang):
    with open('services_json/about.json', mode='r', encoding='UTF-8') as file:
        content = json.load(file)
    if lang == 'en':
        about_info = content['about_en']
    elif lang == 'uz':
        about_info = content['about_uz']
    else:
        about_info = content['about']
    image = content['image']
    return about_info, image

import re

def clean_references(text: str) -> str:
    return re.sub(r'【[^【†]+†[^】]+】', '', text).strip()


