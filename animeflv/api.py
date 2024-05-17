import requests
import bs4
import re
from tqdm import tqdm
from pathlib import Path
import time
import json
#from selenium.webdriver import Firefox, FirefoxOptions

import os
import time


def search_anime(query: str, find_details:bool = True):
    print(f"Searching query: {query}")
    url = f"https://www3.animeflv.net/browse?q={query}"
    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, features="html.parser")

    items = soup.find("ul", {'class': 'ListAnimes'}).find_all('li')
    results = {}

    for item in tqdm(items, desc="Looking up details", unit=' title'):
        title = item.find("h3", {'class': 'Title'}).text
        item_url = item.find('a').attrs['href'].replace('/anime/', "")

        if find_details:
            item_html = requests.get(f"https://www3.animeflv.net/anime/{item_url}").text
            anime_details = re.search(r"var episodes = (?P<list_items>\[.+\]);", item_html).groups('list_items')[0]
            total_chapters = eval(anime_details)[0][0]
        else:
            total_chapters = None

        results[title] = (item_url, total_chapters)

    return results


def find_details(anime_id:str):
    item_html = requests.get(f"https://www3.animeflv.net/anime/{anime_id}").text
    anime_details = re.search(r"var episodes = (?P<list_items>\[.+\]);", item_html).groups('list_items')[0]
    description = bs4.BeautifulSoup(item_html, features="html.parser").find("div", {'class': 'Description'}).text
    total_chapters = eval(anime_details)[0][0]

    return total_chapters, description


def int_to_2_digit_str(num: int):
    if num >= 10: return str(num)
    return "0" + str(num)

def download_one(title: str, chapter: int, output_path: str, return_url:bool=False, override:bool = False, season:int = 1):
    print(f"Downloading {title}-{chapter}")
    
    seasonStr = int_to_2_digit_str(season)
    chapterStr = int_to_2_digit_str(chapter)
    
    
    if season == 0:
        epName = f"{title} E{chapterStr}"
    else:
        epName = f"{title} S{seasonStr}E{chapterStr}"

    if season == 0:
        dirPath = Path(output_path) / f"{title}"
        path = dirPath / f"{title} E{chapterStr}.mp4"
    else:
        dirPath = Path(output_path) / f"{title}" / f"Season {season}"
        path = dirPath / f"{title} S{seasonStr}E{chapterStr}.mp4"
        
    
    if not dirPath.exists():
        dirPath.mkdir(parents=True, exist_ok=True)
    
    if path.exists():
        if not override:
            print("(!) Refusing to override. Pass override=True (--override in the CLI) to force.")
            return

    print("Downloading AnimeFLV.net webpage")
    html = requests.get(f"https://www3.animeflv.net/ver/{title}-{chapter}").text

    print("Getting download URLs")

    soup = bs4.BeautifulSoup(html, features="html.parser")
    lines = str(soup).split("\n")

    for l in lines:
        if l.strip().startswith("var videos = {"):
            break

    l = l.strip()
    
    
    data = json.loads(l[13:-1])
    #print(json.dumps(data, indent=4))
    dataByServer = {}
    
    for d in data["SUB"]:
        dataByServer[d["server"]] = d
        
    downloadComplete = False
    
    if "mega" in dataByServer:
        print("\n===================")
        print("[" + epName + "] Trying backend: MEGA")
        print("===================\n")
        d = dataByServer["mega"]
        command = "mega-get " + str(d["url"]) + " \"" + str(path.absolute()) + "\""
        print("Command:", command)
        code = os.system(command)
        if code == 0:
            downloadComplete = True
    
    
    if not downloadComplete:
        dataByServer.pop("mega")
        for server in dataByServer:
            # sleep 2s - let time for the user to cancel
            time.sleep(2)
            print("\n===================")
            print("[" + epName + "] Trying backend: " + server)
            print("===================\n")
            d = dataByServer[server]
            url = d["url"] if "url" in d else d["code"]
            command = "yt-dlp -o \""+str(path.absolute())+"\" " + str(url)
            print("Command:", command)
            code = os.system(command)
            if code == 0:
                downloadComplete = True
                break
    
    
    if downloadComplete:
        print("[" + epName + "] Download Done")
    else:
        print("[" + epName + "] Download Failed!!!!")
    
    return path
