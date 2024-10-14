# gif_manager.py

import random

gif_urls = [
    "https://media1.tenor.com/m/eQpw7DS4LSwAAAAC/%D0%B1%D0%B0%D0%B1%D0%B0%D0%B5%D0%B2%D1%81%D0%BA%D0%B8%D0%B9.gif",
    "https://media1.tenor.com/m/uWlz-LRz4HAAAAAd/%D0%B1%D0%B0%D0%B9-%D0%B1%D0%B0%D0%B9.gif",
    "https://media.discordapp.net/attachments/768189501918019617/1171558356993974332/prichina.gif"
]

last_gif_url = None

def get_random_gif():
    global last_gif_url
    gif_url = random.choice(gif_urls)
    
    while gif_url == last_gif_url:
        gif_url = random.choice(gif_urls)
    
    last_gif_url = gif_url
    return gif_url
