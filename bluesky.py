from atproto import Client
import os
import requests


def get_post(download_path):
    client = Client()
    profile = client.login('hogehoge.bsky.social', 'password')
    print('Welcome,', profile.display_name)
    
    params = {
        "actor" : client.me.did,
        
    }

    likes = client.app.bsky.feed.get_actor_likes(params=params)
    
    for like in likes:
        if like[0] == 'feed':
            for l in like[1]:
                if l['post']['record']['embed'] is not None:
                    for image in l['post']['record']['embed']['images']:
                        imgurl = 'https://cdn.bsky.app/img/feed_fullsize/plain/' + l['post']['author']['did'] + '/' + image['image'].ref.link + '@jpeg'
                        
                        print(l['post']['author']['display_name'] + ':' + l['post']['record']['text'])
                        
                        download_url(imgurl,download_path,image['image'].ref.link + '.jpg')
        
def download_url(url, download_path, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(os.path.join(download_path, filename), "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
        
if __name__ == '__main__':
    
    # ダウンロード先のフォルダーを指定
    download_path = "./favorite_images"
    
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    get_post(download_path)
