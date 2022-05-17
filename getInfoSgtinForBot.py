# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from autorisation import autorisation
import re
import json





page_autorisation_url = 'https://back-gateway.pharm-portal.ru/sso/login'
login = "sergeykool37@gmail.com"
password = "968577aaa"
sgtin = '04607011634086VABZ2V06A320D'


def get_message_for_bot(sgtin):
    session = autorisation(page_autorisation_url, login, password)
    message = get_info_sgtin(session,sgtin)
    return message

def delete_key_word(string,key_word):
    answer = string.replace(key_word,'')
    return answer

def get_info_sgtin(session,sgtin):
    sgtin_main_info = get_main_info_sgtin(session,sgtin)
    place_of_activity_info = get_place_of_activity_info(session,sgtin_main_info['id_place_of_activity'])
    message = f'Наименование: {sgtin_main_info["name_medicine"]} \n' \
              f'Форма выпуска: {sgtin_main_info["release_from"]} \n' \
              f'МНН: {sgtin_main_info["mnn"]} \n' \
              f'Производитель: {sgtin_main_info["producer"]} \n' \
              f'{sgtin_main_info["number_LU"]} \n' \
              f'{sgtin_main_info["serial_number"]} \n' \
              f'{sgtin_main_info["expiration_date"]} \n' \
              f'{sgtin_main_info["SGTIN"]} \n' \
              f'{sgtin_main_info["SSCC"]} \n' \
              f'{sgtin_main_info["status_SGTIN"]} \n' \
              f'{sgtin_main_info["type_of_emmision"]} \n' \
              f'Идентификатор владельца: {sgtin_main_info["id_place_of_activity"]} \n' \
              f'Наименование организации МД: {place_of_activity_info["org_name_place_of_activity"]} \n' \
              f'ИНН МД: {place_of_activity_info["inn_place_of_activity"]} \n' \
              f'Адрес организации МД: {place_of_activity_info["address_description_place_of_activity"]} \n'

    return message

def get_main_info_sgtin(session, sgtin):
    url_request_sgtin = f'https://sscc.pharm-portal.ru/codes?sgtin={sgtin}'
    get_request_sgtin_main_info = session.get(url_request_sgtin)
    soup_sgtin_main_info = BeautifulSoup(get_request_sgtin_main_info.text, 'lxml')
    div_sgtin_main = soup_sgtin_main_info.find_all('div', re.compile('^styled__Title-sc*'))


    data_main_info_sgtin = dict(
        name_medicine = div_sgtin_main[3].text,
        release_from = div_sgtin_main[5].text,
        mnn=div_sgtin_main[4].text,
        producer=div_sgtin_main[6].text,
        id_place_of_activity=delete_key_word(f'{div_sgtin_main[8].text}','Развернуть'),
        number_LU=f'{div_sgtin_main[10].text} {div_sgtin_main[11].text}',
        serial_number=f'{div_sgtin_main[12].text} {div_sgtin_main[13].text}',
        expiration_date=f'{div_sgtin_main[14].text} {div_sgtin_main[15].text}',
        SGTIN=f'{div_sgtin_main[16].text} {div_sgtin_main[17].text}',
        SSCC=f'{div_sgtin_main[18].text} {div_sgtin_main[19].text}',
        status_SGTIN=f'{div_sgtin_main[20].text} {div_sgtin_main[21].text}',
        type_of_emmision=f'{div_sgtin_main[22].text} {div_sgtin_main[23].text}'
    )

    return data_main_info_sgtin

def get_place_of_activity_info(session,id_place_of_activity):

    url_request_place_of_activity = f'https://back-mdlp.pharm-portal.ru/mdlp/branch/{id_place_of_activity}'
    get_request_place_of_activity_info = session.get(url_request_place_of_activity)
    json_result_request_place_of_activity_info = get_request_place_of_activity_info.content
    data_result_request_place_of_activity_info = json.loads(json_result_request_place_of_activity_info)

    data_place_of_activity_info = dict(
        org_name_place_of_activity=data_result_request_place_of_activity_info['org_name'],
        inn_place_of_activity = data_result_request_place_of_activity_info['inn'],
        address_description_place_of_activity = data_result_request_place_of_activity_info['address_description']
    )


    return data_place_of_activity_info


if __name__ =='__main__':
    print(get_message_for_bot(sgtin))



