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
  
### Installing
```
git clone https://github.com/jidukrishna/spotify_updater.git
```
* Modify the tele_spotify.env with the required parameters and save it

### Executing program on linux

* Installing prerequisites

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
