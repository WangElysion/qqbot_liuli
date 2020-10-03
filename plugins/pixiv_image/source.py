#encoding=utf-8
import requests, re, bs4, os, shutil, json, random

IMAGR_DATA_PATH = "data/pixiv/img_data"
ARTIST_DATA_PATH = "data/pixiv/aritsts"
IMAGE_PATH = "image/pixiv"
DOWNLOAD_IMG = "https://pixiv.cat/"
ILEAGEL_CHAR = '\\/\":*?<>|'
cwd=os.getcwd()
TRANS_TABLE1 = str.maketrans("", "", ILEAGEL_CHAR)
header = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    "authorization": "eyJhbGciOiJIUzUxMiJ9.eyJwZXJtaXNzaW9uTGV2ZWwiOjEsInJlZnJlc2hDb3VudCI6MSwiaXNCYW4iOjEsInVzZXJJZCI6MTg1ODA1LCJpYXQiOjE2MDEyMjE1MzYsImV4cCI6MTYwMjk0OTUzNn0.CdzvWY6miKlkE_I_PmW18UaKHGhLku59cndONvH6Ol5cLmXq_KIdBNq-JEdRrufRz0S7KLAMWM9N4pG3taz6zA"}


async def pic_send(n:int):
    """
    用于发送图片
    """
    msg_list=[]
    pic_num_remain=len(listdir(IMAGE_PATH))
    file_paths=random.choices(listdir(IMAGE_PATH),k=n)
    cwd = os.getcwd()
    for pic_path in file_paths:
        file_url="file:///"+os.path.join(cwd,pic_path)
        image_msg="[CQ:image,file={}]".format(file_url)
        msg_list.append(image_msg)
    msg="\n".join(msg_list)
    return msg,file_paths,pic_num_remain



def pic_order_update(artistID: str) -> str:
    """
    用于指定作者订阅更新
    """
    data = []
    page = 1
    while True:
        res = requests.get(
            url="https://api.pixivic.com/artists/{1}/illusts/illust?page={0}&pageSize=30".format(page, artistID),
            headers=header,
            timeout=60
        )
        info = res.json()
        for pic_info in info['data']:
            for urls in pic_info["imageUrls"]:
                type = urls['original'].split('.')[-1]
                break
            pic_data = {
                "title": pic_info['title'],
                "id": pic_info['id'],
                "count": pic_info['pageCount'],
                "type": type
            }
            data.append(pic_data)
        if len(info['data']) < 30:
            break
        page += 1
    with open("{}/{}.json".format(IMAGR_DATA_PATH, artistID), "w+", encoding="utf-8") as f:
        json.dump(data, f)
    return "{}更新成功".format(artistID)
    pass


def pic_reload() -> None:
    """
    在图片中低于某个值时,从网站下载图片补充至40
    """
    image_count_remain = len(listdir(IMAGE_PATH))
    img_data = []
    for path in listdir(IMAGR_DATA_PATH):
        with open(path) as f:
            img_data += json.load(f)
    for data in random.choices(img_data, k=50 - image_count_remain):
        if data["count"] == 1:
            filename = "{}/{}.{}".format(IMAGE_PATH,  data['id'], data['type'])
            url_download = "{}/{}.{}".format(DOWNLOAD_IMG, data['id'], data['type'])
            downlaod(url_download=url_download, filename=filename)
        else:
            for num in range(1, int(data['count']) + 1):
                filename = "{}/{}_{}.{}".format(IMAGE_PATH,  data['id'], num,
                                                   data['type'])
                url_download = "{}/{}-{}.{}".format(DOWNLOAD_IMG, data["id"], num, data['type'])
                downlaod(url_download=url_download, filename=filename)


async def pic_order_update_all():
    with open(os.path.join(ARTIST_DATA_PATH, "artist.txt"),"r+",encoding="utf-8") as f:
        for artisrtID in f.readlines():
            try:
                pic_order_update(artistID=artisrtID[-1])
            except:
                continue
    msg = "更新成功"
    return msg

async def add_order(artistID):
    with open(os.path.join(ARTIST_DATA_PATH, "artist.txt"), "a+") as f:
        f.write(artistID+'\n')
    pic_order_update(artistID)

def mkdir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def listdir(directory: str) -> list:
    file_paths = []
    for root, dir, File in os.walk(directory):
        del dir
        for f in File:
            file_paths.append(os.path.join(root, f))
    return file_paths


def downlaod(url_download: str, filename) -> None:
    with requests.get(url_download, stream=True) as repo:
        with open(filename, "wb+") as f:
            for chunk in repo.iter_content(chunk_size=512):
                f.write(chunk)

def delete(file_paths:list):
    for path in file_paths:
        if os.path.exists(path):
            os.remove(path)

if __name__ == '__main__':
    mkdir(IMAGR_DATA_PATH)
    mkdir(ARTIST_DATA_PATH)
    mkdir(IMAGE_PATH)
    print(pic_order_update("1023317"))
    pic_reload()
