import requests
from pprint import pprint


TOKEN_YA = ''
TOKEN_VK = ''
user = ''


class VkUser():
    def __init__(self, token_ya):
        self.token_ya = token_ya

    def get_photos_dict(self,user_id):
        self.user_id = user_id
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': TOKEN_VK,
            'v': '5.131',
            'owner_id': user,
            'album_id': 'profile',
            'photo_sizes': 1,
            'extended': 1,
            'rev': 0,
            'count': 500
        }
        req = requests.get(url, params=params).json()
        postlist = req['response']['items']
        photo_dict = {}
        for dict in postlist:
            for i in dict['sizes']:
                if i['type'] == 'z':
                    if str(dict['likes']['count'])+'.jpg' in photo_dict.values():
                        photo_dict[i['url']] = str(dict['likes']['count']) + 'date' + str(dict['date']) + '.jpg'
                    else:
                        photo_dict[i['url']] = str(dict['likes']['count']) +'.jpg'
        return  photo_dict


    def upload_files(self, user_id,count=5):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token_ya)
        }
        photo_dict = self.get_photos_dict(user_id=user_id)
        for image in photo_dict.items():
            if count == 0:
                break
            else:
                url_d = image[0]
                with open(image[1], 'wb') as file:
                    res = requests.get(url_d)
                    file.write(res.content)
                params = {
                'path' : f'Загрузки/{image[1]}',
                'overwrite' : 'true'
                }
                resp = requests.get(files_url, headers=headers, params=params)
                url = resp.json()['href']
                count -= 1
                response = requests.put(url, data=open(image[1], 'rb'))
                response.raise_for_status()
        return 'Успешно'



user_vk = VkUser(TOKEN_YA)
pprint(user_vk.upload_files(user))

