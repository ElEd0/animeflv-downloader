
# AnimeFLV.net downloader


> fork of https://github.com/apiad/animeflv-downloader

This script is very simple, it will attempt to download video files from [AnimeFLV.net](https://animeflv.net).
It also works as Telegram Bot!

> **DISCLAIMER:** This project is for personal and legitimate use ONLY. It is not designed for commercial use. 
> I do not endorse blatanly downloading copyrighted material from anywhere in the Internet.
> That being said, if you are from a Third World country where this content is simply not available, you only have an intermitent or unreliable Internet connection, and the content is only for your personal consumption, that can be considered a legitimate use.
>
> Please support [AnimeFLV.net](https://animeflv.net) in any way you can. Specially, do visit the website and watch the chapters through streaming if you can afford it. They make an awesome job and they deserve your support.

### How it works

This fork completely changes how the script downloads videos. Instead of looking for a goCDN URL and download the stream using python, it uses a combination of existing tools (megaCMD and yt-dlp) and tries to download the episodes from the listed servers. If the file is not found in the first server (mega, usually) it tries the next one, and so on.

This makes the program heavier but it also makes it more reliable and future proof. Another added benefit is that it does'nt use selenium anymore so it does'nt require an x server, making it easier to run on a headless machine.


### Install
##### Docker
The recommended way of running the script is using docker, that way you dont have to deal with dependencies. Just build the image from the repo

```
docker build -t ed0/animeflv-dler .
```

Execute a command in a new container, create volume for `/src/output` which is the default download location

```
docker run --rm -it -v ./output:/src/output ed0/animeflv-dler python3 -m animeflv --help
```

##### Bare metal
Install the dependencies
- [megaCMD](https://github.com/meganz/MEGAcmd)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

Then clone repo, cd to the root of the project, optionally create a virtualenv, and then run:
```
pip install -r requirements.txt
```

### Usage

Pass the title of an anime series as it appears in the URL. For example, for <https://www3.animeflv.net/anime/shingeki-no-kyojin> the title is `shingeki-no-kyojin`, and optionally the initial and final episode:

```
python -m animeflv download shingeki-no-kyojin 1 25 [--output_path <path>]
```

If you don't know the exact URL, try `search`:
```
python -m animeflv search "shingeki no kyojin"
```

It will print something like:

   Shingeki no Kyojin: Kuinaki Sentaku [2 chapters] ( shingeki-no-kyojin-kuinaki-sentaku )
   Shingeki no Kyojin Season 2 [12 chapters] ( shingeki-no-kyojin-season-2 )
   Shingeki no Kyojin OVA [3 chapters] ( shingeki-no-kyojin-ova )
   Shingeki no Kyojin Season 3 [12 chapters] ( shingeki-no-kyojin-season-3 )
   Shingeki no Kyojin Live Action [1 chapters] ( shingeki-no-kyojin-live-action )
   Shingeki no Kyojin Movie 1: Guren no Yumiya [1 chapters] ( shingeki-no-kyojin-movie-1-guren-no-yumiya )
   Shingeki no Kyojin Movie 2: Jiyuu no Tsubasa [1 chapters] ( shingeki-no-kyojin-movie-2-jiyuu-no-tsubasa )
   Shingeki no Kyojin [25 chapters] ( shingeki-no-kyojin )
   Shingeki no Kyojin: Chimi Kyara Gekijou - Tondeke! Kunren Heidan [9 chapters] ( shingeki-no-kyojin-chimi-kyara-gekijou-tondeke )
   Shingeki no Kyojin Season 3 Part 2 [10 chapters] ( shingeki-no-kyojin-season-3-part-2 )
   Shingeki no Kyojin: Lost Girls [3 chapters] ( shingeki-no-kyojin-lost-girls )

After seeing the search results, if you want to simply download **all chapters** from **all the listed anime**, just type:
```
python -m animeflv search <query> --download_all
```

> WARNING: This option can download A LOT of episodes sometimes. Use with care.

#### Download path
The episodes will download at the location `output/<anime-title>/Season <season>/<anime-title> S<season>E<episode>.mp4` This is the [directory structure recommended by Jellyfin](https://jellyfin.org/docs/general/server/media/shows/), it also works nice with Plex, I recommend adding `[imdbid-<show-id>]` to the end of the anime folder name.
The script tries to guess the season from the anime title (eg. shingeki-no-kyojin-2, season=2), but the format can be different so you can define the season number by passing argument `--season=<season>`.
Using `--season=0` will change the download location to `output/<anime-title>/<anime-title> E<episode>.mp4`, recommended for movies.

### Telegram Bot

If you want to run the Telegram bot (you should know what you're doing):

```
python -m animeflv.bot <TOKEN>
```

The bot requires `MP4Box` installed, in Debian-based distributions (Ubuntu) this app is the `gpac` package.
Also, `zip` is required.

```
apt install -y gpac zip
```

##### Docker

If you prefer docker, running the bot it is even easier:

```
TOKEN=<your-token> docker-compose up -d
```
