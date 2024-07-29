# Spotify Playlist Updater and Shuffler via Telegram

A telegram bot to update or shuffle a playlist with songs from liked and shazam playlist.

## Description

A simple telegram bot that updates a main playlist (you have to make one) with your liked and shazam playlist. 
This script makes use of spotipy and python-telegram-bot api inorder to achieve the task.
The update option filters the extra songs from liked and shazam playlists and adds to the main playlist.
The shuffle option updates and shuffles the main playlist.
Alive option responds if the bot is online
/all command gives the all songs in main_songs table in the database in a csv file

## Getting Started
<h3>Spotify setup</h3>
1. Create a spotify app <a href="https://developer.spotify.com/dashboard" target="_blank">Spotify Dashboard</a> <br>
2. Put the Redirect URIs as http://google.com/callback/ in the spotify app.<br>
3. Make sure to copy down the client id and client secret.<br>
4. Copy the shazam playlist id (make sure its private).<br>
5. Make a private playlist and copy its id.<br>

<h3>Telegram setup</h3>
1. Create bot using <a href="https://t.me/BotFather" target="_blank">@BotFather</a>.<br>
2. U can use /help and follow the instructions to set up a new bot.<br>
3. Copy the token id.<br>
4. Using <a href="https://t.me/RawDataBot" target="_blank">@RawDataBot</a> find your chat id copy it down.<br>

### Dependencies

* Python3
  
### Cloning repo
```
git clone https://github.com/jidukrishna/spotify_updater.git
```
* Modify the tele_spotify.env with the required parameters and save it

### Executing program on linux

* Installing prerequisites
  ```
  cd spotify_updater
  python -m venv venv
  . venv/bin/activate
  pip install -r requirements.txt
  ```
* Running it
  ```
  python tele_spotify.py
  ```
* When you run for the first time a redirect url will be shown or logged into the terminal copy and paster in the given field.
* After that start the bot and click on update to build the database
* That's it (❁´◡`❁)


### Executing program on windows

* Installing prerequisites
  ```
  cd spotify_updater
  python -m venv venv
  venv/scripts/activate
  pip install -r requirements.txt
  ```
* Running it (with the activated env)
  ```
  python tele_spotify.py
  ```
* When you run for the first time a redirect url will be shown or logged into the terminal copy and paster in the given field.
* After that start the bot and click on update to build the database
* That's it (❁´◡`❁)

### Run on reboot for pi
* Create a sh_spotify.sh file in spotify_updater folder and replace the necessary things
  ```
  #!/bin/bash
  
  source /home/<user_name>/spotify_updater/venv/bin/activate
  
  sleep 5
  cd /home/<user_name>/spotify_updater
  nohup python tele_spotify.py > /dev/null 2>&1 &
  ```
* Making it a executable
  ```
  sudo chmod +x sh_spotify.sh
  ```
* Adding to crontab for running on reboot
  ```
  sudo crontab -e 
  ```
* add this line at end of the file with your shell script path
  ```
  @reboot /home/<user_name>/spotify_updater/sh_spotify.sh
  ```
* reboot the pi ```sudo reboot```

## Help
* It may take a few tries to get the spotify redirect url working.
* Make sure your running from the correct path.
* You can always see the logs and figure it out

## Author 🗿
Jidu Krishna P J <br>
Instagram : [@jidukrishnapj](https://www.instagram.com/jidukrishnapj/) <br>
Github : [@jidukrishna](https://github.com/jidukrishna)

## Version History

* 0.1
    * Initial Release

## License

```
Copyright [2024] [Jidu Krishna P J]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Made with help of
* [python-telegram-bot](https://python-telegram-bot.org/)
* [spotipy](https://pypi.org/project/spotipy/)
