import requests
import json
import os

token = '143531255696f335289513cfe1070910d70abce70a4bd5b47e6514a15e10755e2f26e34563ca60b096ac9'
base = 'https://api.vk.com/method/'
method_api = 'photos.get'
album_id = 'profile'
photo_sizes = True
version_app = 5.101
need_system = True
array_id = []


"""Reading file id.txt"""
f = open('id.txt', encoding='UTF-8')
"""Add id users in array_id"""
for line in f.readlines():
    array_id.append(line)
f.close()

"""Split elements in array_id for \n"""
array_id = [line.rstrip() for line in array_id]

def add_dir_for_photos():
    for i in array_id:
        os.mkdir(f'id{i}')

def get_owner_id():
    for owner_id in array_id:
        return owner_id

def write_json(data):
    # with open('photos.json', 'w') as file:
    with open(f'id{get_owner_id()}/' + 'photos.json', 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def get_largest(size_dict):
    if size_dict['width'] >= size_dict['height']:
        return size_dict['width']
    else:
        return size_dict['height']

def download_photo(url):
    for owner_id in array_id:
        r = requests.get(url, stream = True)
        filename = url.split('/')[-1]
        with open(f'id{get_owner_id()}/' + filename, 'wb') as file:
            for chunk in r.iter_content(4096):
                file.write(chunk)

def main():
    add_dir_for_photos()

    for owner_id in array_id:

        r = requests.get(base + method_api, params = {'access_token': token,
                                                      'owner_id': owner_id,
                                                      'v': version_app,
                                                      'album_id': album_id,
                                                      'photo_sizes': photo_sizes})
        write_json(r.json())

        photos = json.load(open(f'id{get_owner_id()}/' + 'photos.json'))['response']['items']

        for photo in photos:
            sizes = photo['sizes']

            max_size_url = max(sizes, key = get_largest)['url']
            download_photo(max_size_url)


if __name__ == '__main__':
    main()
