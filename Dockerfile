FROM ubuntu:22.04


RUN apt-get update \

    # Upgrade
    && apt-get upgrade -y \
    && apt-get dist-upgrade -y \

    # Install dependencies
    && apt-get install -y wget gpac python3 python3-pip python-is-python3 zip yt-dlp \
	

    # Download & Install MegaCMD
    && wget https://mega.nz/linux/repo/xUbuntu_22.04/amd64/megacmd-xUbuntu_22.04_amd64.deb \
    && (dpkg -i megacmd-xUbuntu_22.04_amd64.deb || true) \
    && apt-get install -f -y \
    && mkdir /root/MEGA \


    # Cleanup
    && rm *.deb \
    && apt-get purge -y \
    && apt-get autoremove -y \
    && apt-get autoclean -y \

	&& useradd anime


# Install animeflv-downloader
COPY requirements.txt /src/requirements.txt
WORKDIR /src
RUN python3 -m pip install -r requirements.txt
COPY animeflv /src/animeflv
USER anime
