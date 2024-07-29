import logging
import sqlite3
import time
import traceback
import csv
import spotipy
from dotenv import dotenv_values
from spotipy.oauth2 import SpotifyOAuth
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

config=dotenv_values("tele_spotify.env")
playist_id_main = config["spotify_playist_id_main"] #playlist id to add the songs private
shazam_playlist_id = config["spotify_shazam_playlist_id"]  # your private shazam playlists
client_id = config["spotify_client_id"] # spotify client id
client_secret = config["spotify_client_secret"]  # spotify client secret
chat_id_tele = int(config["telegram_chat_id"])  # telegram chat id
bot_token=config["telegram_bot_token"] #telegram bot token
name_owner=config["your_name"]

#keyboard buttons
replies = ["♫Shuffle🔀", "🎧Update↻"]
keyboard = ReplyKeyboardMarkup([replies,["Alive💀???"]], one_time_keyboard=False, resize_keyboard=True)



# use for logging telegram logs (uncomment for telegram logs)
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )

#spotify authentication

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://google.com/callback/",
                                               scope="user-read-playback-state,playlist-modify-private"))


#ping google for checking network incase wifi is down


# func for resetting the tables
def reset_db(table_name='all_spotify_user.db'):
    with sqlite3.connect('all_spotify_user.db', check_same_thread=False) as db:
        db.execute("create table if not exists songs (no INTEGER PRIMARY KEY,uri text UNIQUE,song text)")
        db.execute("create table if not exists main_songs (no INTEGER PRIMARY KEY,uri text UNIQUE,song text)")
        if table_name == 'all_spotify_user.db':
            db.execute("delete from songs")
        else:
            db.execute("delete from main_songs")


# code to update the local database consisting of the songs
def add_to_database(playlist="", table_name='all_spotify_user.db', liked=False, resetcondition=False):
    try:

        # reset the table once to avoid accidental clearing
        if resetcondition:
            reset_db("main_list_data")
            reset_db()

        # from down here its a systematic collecting of songs using the offsets and limits
        offset_value_increment = 0
        song_counter_playlist = 0
        check_songs = True
        first_song_name = ""
        while check_songs:

            # liked option controls the connection between liked songs and playlists
                if liked:
                    value = 50
                    while True:
                        try:
                            spotify_obj = sp.current_user_saved_tracks(limit=value, offset=offset_value_increment)
                            break
                        except TimeoutError:
                            time.sleep(3)
                else:
                    while True:
                        try:
                            spotify_obj = sp.playlist_items(playlist, limit=100, offset=offset_value_increment)
                            break
                        except TimeoutError:
                            time.sleep(3)

                    value = 100
                offset_value_increment += value

                # this is simply for debugging purpose
                if offset_value_increment == value:
                    first_song_name = spotify_obj["items"][0]["track"]["name"]

                # to check if it's finished or not
                if len(spotify_obj["items"]) == 0:
                    break

                # adding to db
                for i in spotify_obj["items"]:
                    song_counter_playlist += 1
                    song_name = i["track"]["name"]
                    uri = i["track"]["uri"]
                    if song_name == "" and table_name == "all_spotify_user.db":
                        continue
                    with sqlite3.connect("all_spotify_user.db", check_same_thread=False) as db:
                        cur = db.cursor()
                        cur.execute("insert or ignore into songs values (NULL,?,?)", (uri, song_name))
                    # adds in the main_songs table for updation in the main list
                    if resetcondition:
                        with sqlite3.connect('all_spotify_user.db', check_same_thread=False) as db:
                            cur = db.cursor()
                            cur.execute("insert or ignore into main_songs values (NULL,?,?)", (uri, song_name))


    except Exception as e:
        print(traceback.format_exc())
        return (False, e, False)

    return first_song_name, song_name, song_counter_playlist


# uses the existing main_songs tables and clear the spotify playlist and adds it randomly
def randomize_songs():
    try:
        #add controls the adding and removing key
        def playlist_mod(add=False):
            filename = "all_spotify_user.db"
            with sqlite3.connect(filename, check_same_thread=False) as db:
                cur = db.cursor()
            if add:
                cur.execute("select uri from songs order by random()")
            else:
                cur.execute("select uri from songs")
            song_counter = 0
            uri_list = []
            playlist = playist_id_main
            #systematic removal and adding of songs
            for i in cur:
                song_counter += 1
                uri_list.append(i[0])
                if song_counter == 99:
                    song_counter = 0
                    if add and uri_list:
                        print(len(uri_list))
                        while True:
                            try:
                                sp.playlist_add_items(playlist, uri_list)
                                break
                            except  TimeoutError:
                                time.sleep(3)

                    elif uri_list:
                        while True:
                            try:
                                sp.playlist_remove_all_occurrences_of_items(playlist, uri_list)
                                break
                            except TimeoutError:
                                time.sleep(3)


                    uri_list = []
            else:
                if add and uri_list:
                    print(len(uri_list))
                    while True:
                        try:
                            sp.playlist_add_items(playlist, uri_list)
                            break
                        except TimeoutError:
                            time.sleep(3)
                elif uri_list:
                    while True:
                        try:
                            sp.playlist_remove_all_occurrences_of_items(playlist, uri_list)
                            break
                        except TimeoutError:
                            time.sleep(3)

        playlist_mod()
        playlist_mod(True)
        return {"status": True}
    except Exception as e:
        return {"status": False, "prob": (f"yo bro we got some problem : {e}")}


# count the no of rows in table
def db_row_count(table="songs"):
    with sqlite3.connect("all_spotify_user.db", check_same_thread=False) as db:
        cur = db.cursor()
        k = cur.execute(f"select count(uri) from {table}").fetchone()[0]
        return k


# add the new songs into the playlist at top without messing up
def add_extra():
    with sqlite3.connect("all_spotify_user.db", check_same_thread=False) as db:
        cur = db.cursor()
        cur.execute(
            "select uri,song from songs as n where not exists(select * from main_songs as m where m.uri=n.uri) ")
        uri = []
        names = []
        for i in cur:
            print(i)
            uri.append(i[0])
            names.append(i[1])
            print(i[1])
        while True:
            try:
                sp.playlist_add_items(playist_id_main, uri, position=0)
                break
            except TimeoutError:
                time.sleep(3)

        name_str = ',\n'.join(names)
        return f"{name_owner} sensei we have added ur requested {len(names)} songs :\n{name_str}"


# the 1st main command for updating and adding in one go

def update_database():
    try:
        current = add_to_database(playist_id_main, resetcondition=True, table_name="main_list_data"
                                                                                   "")[-1]
        v2=add_to_database(shazam_playlist_id)[-1]
        v3=add_to_database(liked=True)[-1]
        print(current,v2,v3)
        print(current+v3+v2)
        new = db_row_count()
        diff = new - current
        if diff > 0:
            value = add_extra()
            return {"status": True, "data": value}
        return {"status": True, "data": "no data to be added"}

    except Exception as e:
        return {"status": False, "data": e}


# the 2nd main command for randomising the playlist
def update_rand():
    try:
        k = update_database()

        mssg = ""
        if k["status"]:
            mssg += k["data"] + " "
        else:
            return "some prob sensei" + k["data"]
        print(mssg)
        k = randomize_songs()
        if k["status"]:
            return mssg + f"\nYour playlist is shuffled sensei {name_owner}"
        else:
            return "some prob sensei" + k["prob"]

    except Exception as e:
        print(traceback.format_exc())
        return e


# returns the songs in a csv format
def all_songs():
    with sqlite3.connect("all_spotify_user.db", check_same_thread=False) as db:
        cur = db.cursor()
        k = cur.execute(f"select no,song,uri from main_songs order by no")
        with open("songs_list.csv","w",newline="\n",encoding="utf-8") as f:
            krit=csv.writer(f)
            krit.writerow(["no","song","uri"])
            for i in k:
                krit.writerow(i)
        return




#user verification
def check_user(k: Update):
    if k.message.chat_id == chat_id_tele:
        return True
    return False


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if check_user(update):
        mssg = f"Welcome back {name_owner} sensei🥷🏼? how can i help u today 🙇🏽‍♀️....."
        while True:
            try:
                await update.message.reply_text(mssg, reply_markup=keyboard)
                break
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(3)
    else:
        name = update.message.chat.first_name
        while True:
            try:
                await update.message.reply_text(
                    f"https://cataas.com/cat/says/nee%20aarada%20{name}%20bhai?fontSize=50&fontColor=white")
                break
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(3)



async def all_spotify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if check_user(update):
        while True:
            try:
                all_songs()
                await update.message.reply_document("songs_list.csv",reply_markup=keyboard)
                break
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(3)

    else:
        name = update.message.chat.first_name
        while True:
            try:
                await update.message.reply_text(
                    f"https://cataas.com/cat/says/nee%20aarada%20{name}%20bhai?fontSize=50&fontColor=white")
                break
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(3)






async def shuffle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_user(update):
        name = update.message.chat.first_name
        while True:
            try:
                await update.message.reply_text(
                    f"https://cataas.com/cat/says/nee%20aarada%20{name}%20bhai?fontSize=50&fontColor=white")
                break
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(3)

    if update.message.text == "♫Shuffle🔀":
        k = update_rand()
        while True:
            try:
                await update.message.reply_text(k,reply_markup=keyboard)
                break
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(3)

    elif update.message.text == "🎧Update↻":
        k = update_database()["data"]
        print(k)
        while True:
            try:
                await update.message.reply_text(k,reply_markup=keyboard)
                break
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(3)
    elif update.message.text == "Alive💀???":
        while True:
            try:
                await update.message.reply_text(f"Very much alive {name_owner} sensei.\nAll i care is your health❤️‍🩹"
                                                ,reply_markup=keyboard)
                break
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(3)



    else:
        while True:
            try:
                await update.message.reply_text(f"{name_owner} sensei the command you typed doesn't exists",reply_markup=keyboard)
                break
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(3)



async def data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_user(update):
        name = update.message.chat.first_name
        while True:
            try:
                await update.message.reply_text(
                    f"https://cataas.com/cat/says/nee%20aarada%20{name}%20bhai?fontSize=50&fontColor=white")
                break
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(3)
    while True:
        try:
            await update.message.reply_text(f"{name_owner} sensei the message u sent rn doesn't exists",reply_markup=keyboard)
            break
        except Exception as e:
            logging.error(f"error : line 362 {e}")
            time.sleep(3)



def main():
    app = (Application.builder()
           .token(bot_token)
           .read_timeout(30)
           .write_timeout(30)
           .build())
    app.add_handler(CommandHandler("start", welcome))
    app.add_handler(CommandHandler("all", all_spotify))
    app.add_handler(MessageHandler(filters.Text(replies+["Alive💀???"]), shuffle))
    app.add_handler(MessageHandler(filters.CHAT, data))
    app.run_polling(allowed_updates=Update.ALL_TYPES)
if __name__ == "__main__":
    main()
