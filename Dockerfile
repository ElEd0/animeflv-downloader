FROM ubuntu:22.04


RUN apt-get update \

    # Upgrade
    && apt-get upgrade -y \
    && apt-get dist-upgrade -y \

    # Install dependencies
    && apt-get install -y wget gpac firefox python3 python3-pip zip yt-dlp \
	

    # Download & Install MegaCMD
    && wget https://mega.nz/linux/repo/xUbuntu_22.04/amd64/megacmd-xUbuntu_22.04_amd64.deb \
    && (dpkg -i megacmd-xUbuntu_22.04_amd64.deb || true) \
    && apt-get install -f -y \


    # Cleanup
    && rm *.deb \
    && apt-get purge -y \
    && apt-get autoremove -y \
    && apt-get autoclean -y \

    && mkdir /root/MEGA


# Install animeflv-downloader
COPY requirements.txt /src/requirements.txt
WORKDIR /src
RUN python3 -m pip install -r requirements.txt
COPY animeflv /src/animeflv
