import aiohttp
import requests
import asyncio
import aiofiles
import PIL
from PIL import Image

url = 'http://142.93.138.114/images/'
response = requests.get('http://142.93.138.114/images/')
image_names = response.text

list_names = image_names.splitlines()
u = list()
for i in list_names:
    addres = "http://142.93.138.114/images/" + i
    u.append(addres)

async def make_filename(session, url):
    response = await session.request(method="GET", url=url)
    filename = url.split('/')[-1]
    async for data in response.content.iter_chunked(1024):
        async with aiofiles.open(filename, "ba") as f:
            await f.write(data)
    return filename

async def get_images():
    urls = u
    async with aiohttp.ClientSession() as session:
        coros = [make_filename(session, url) for url in urls]
        result_files = await asyncio.gather(*coros)
    return result_files

async def mirror_image(list_names):
    for i in list_names:
        im = Image.open(i)
        out = im.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        out.save(i)
    return True

async def post_images(list_names):
    print(len(list_names))
    for i in list_names:
        files = {i: open(i, 'rb')}
        req_post = requests.post('http://142.93.138.114/images/', files = files)

def main():
    asyncio.run(get_images())
    asyncio.run(mirror_image(list_names))
    post_images(list_names)

if __name__ == '__main__':
    main()








