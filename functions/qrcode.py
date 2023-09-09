from ldubgdbot.bot.utils.env import Env
import requests
import json


def _get_file(file_id):
    get_file_api_url = f'https://api.telegram.org/bot{Env.TOKEN}/getFile'
    get_file_content_api_url = f'https://api.telegram.org/file/bot{Env.TOKEN}/' + '{file_path}'
    response = requests.post(url=get_file_api_url, params={'file_id': file_id})
    json_response = json.loads(response.content)
    if response.status_code != 200 or not json_response.get('ok'):
        raise FileNotFoundError()
    response = requests.get(url=get_file_content_api_url.format(file_path=json_response['result']['file_path']))
    if response.status_code != 200:
        raise FileNotFoundError()
    return response.content
