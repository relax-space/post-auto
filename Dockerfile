FROM python:3.9.1
RUN echo 'deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster main contrib non-free \n \
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-updates main contrib non-free \n \
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ buster-backports main contrib non-free \n \
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security buster/updates main contrib non-free' > /etc/apt/sources.list
RUN cat /etc/apt/sources.list
RUN apt update
RUN apt install -y chromium
RUN apt install -y tesseract-ocr
RUN apt install -y gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget libcairo-gobject2 libxinerama1 libgtk2.0-0 libpangoft2-1.0-0 libthai0 libpixman-1-0 libxcb-render0 libharfbuzz0b libdatrie1 libgraphite2-3 libgbm1
