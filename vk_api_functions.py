import requests

VK_API_VERSION = '5.131'


def get_wall_upload_server(group_id, access_token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    post_data = {
        'group_id': group_id,
        'access_token': access_token,
        'v': VK_API_VERSION
    }
    response = requests.post(url, data=post_data)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_photo_to_server(img_path, upload_url, group_id, access_token):
    with open(img_path, 'rb') as file:
        files = {'photo': file}
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    response_info = response.json()
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    post_data = {
        'group_id': group_id,
        'photo': response_info['photo'],
        'server': response_info['server'],
        'hash': response_info['hash'],
        'access_token': access_token,
        'v': VK_API_VERSION
    }
    response = requests.post(url, data=post_data)
    response.raise_for_status()
    vk_server_data = response.json()
    return {
        'owner_id': vk_server_data['response'][0]['owner_id'],
        'media_id': vk_server_data['response'][0]['id']
    }


def post_on_wall(vk_server_data, group_id, access_token, text):
    url = 'https://api.vk.com/method/wall.post'
    post_data = {
        'owner_id': -group_id,
        'from_group': 1,
        'attachments': f"""photo{vk_server_data['owner_id']}
                        _{vk_server_data['media_id']}""",
        'message': text,
        'access_token': access_token,
        'v': VK_API_VERSION
    }
    response = requests.post(url, data=post_data)
    response.raise_for_status()
