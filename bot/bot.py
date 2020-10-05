import os
import csv
import sqlite3
import logging
import telegram
from datetime import datetime
from dotenv import load_dotenv
from helpers.helpers import DATE_PATTERN, NUMBER_TO_MONTH, md_to_img
from telegram.parsemode import ParseMode
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters


# TODO 
# - [ ] 


logging.basicConfig(
    filename="logs.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)



class VaishnaBot():
    load_dotenv()
    def __init__(self):

        self.logger = logging.getLogger(name="vaishnabot")

        self.updater = Updater(token=os.getenv("BOTKEY"), use_context=True)
        
        self.updater.dispatcher.add_handler(CommandHandler("start", self.start))
        self.updater.dispatcher.add_handler(CommandHandler("ekadasi", self.ekadasi_event))
        self.updater.dispatcher.add_handler(CommandHandler("iskcon_events", self.iskcon_event))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.message_handler))

        self.updater.start_polling() 

        print("Vaishnabot initialized!")

        self.updater.idle()
        

    def start(self, update, context):
        print(update.message)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hari Bol! Hare Krishna! I'm Vaishnabot")


    def message_handler(self, update, context):
        username = update.message.chat.username 
        human_said = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"You {username} said: {human_said}")


    def ekadasi_event(self, update, context):
        """
            Get the ekadasi events by:
                * month (argument)
                    * current year (default)
                    * specified by user (argument)
                * year (argument)
                * default: all from current year

            The dates sent by the user must be in the formats: 
                mm-YYYY
                YYYY-mm
                YYYY
                mm (current year)
                
                months are allowed to be numbers 1-12 or strings (january, ..., december)
        """
        self.logger.info("User {} requested /ekadasi command".format(update.message.chat.username))
                
        if not context.args: 
            context.bot.send_message(chat_id=update.effective_chat.id, text="I'll show you the Ekadasi dates for this year")
            current_year = datetime.today().year

            body = "# Ekadasi dates for this year"

            events = self.get_ekadasi_events(current_year, fetch_by="year")

            for event in events:
                body += f"\n## {event[1]}\n\n"
                body += f"Month: {event[3]}\n"
                body += f"Day: {event[2]}\n"
                body += f"Year: {event[4]}\n"
                body += f"Starts: {event[5]}\n"
                body += f"Ends: {events[6]}\n"
                
            print(body)
            
            context.bot.send_message(chat_id=update.effective_chat.id, text=body, parse_mode=ParseMode.MARKDOWN_V2)

        else: 
            ekadasi_date = "".join(context.args)
            if DATE_PATTERN.fullmatch(ekadasi_date):
                year, month = None, None

                for date in ekadasi_date.split("-"):
                    if len(date) == 2:
                        month = NUMBER_TO_MONTH[int(date)]
                    elif len(date) == 4:
                        year = int(date)
                
                if year and month:
                    body = f"# Ekadasi events for {month}-{year}\n"
                    events = self.get_ekadasi_events([month, year], fetch_by="month&year")

                elif year:
                    body = f"# Ekadasi events for {year}\n"
                    events = self.get_ekadasi_events(year, fetch_by="year")

                elif month:
                    body = f"# Ekadasi events for {month}\n"
                    events = self.get_ekadasi_events(month, fetch_by="month")
                
                for event in events:
                    print(event)
                    body += f"\n## {event[1]}\n\n"
                    body += f"Month: {event[3]}\n"
                    body += f"Day: {event[2]}\n"
                    body += f"Year: {event[4]}\n"
                    body += f"Starts: {event[5]}\n"
                    body += f"Ends: {event[6]}\n"


                body_md_img = md_to_img(body)


                context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=body_md_img)

            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Make sure to enter a valid date")            
        
    def iskcon_event(self, update, context):
        """
            Get the iskcon events by:
                * month (current year)
                * year
                * default: all from current year
        """

        self.logger.info("User {} requested /iskcon_events command".format(update.message.chat.username))

        if not context.args:
            current_year = datetime.today().year
            body = f"# Iskcon {current_year} events\n"
            events = self.get_iskcon_events(current_year, fetch_by="year")
            
            for event in events:
                body += f"\n## {event[1]}\n\n"
                body += f"+ Year: {event[4]}\n"
                body += f"+ Month: {event[2]}\n"
                body += f"+ Day: {event[3]}\n"
            
            context.bot.send_message(chat_id=update.effective_chat.id, text="I'll send you the iskcon events")
            # context.bot.send_message(chat_id=update.effective_chat.id, text=body)
            body_md_img = md_to_img(body)
            body_md_img.seek(0)
            print(body_md_img)
            # body_md_img.show()

            context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=body_md_img)

        else: 
            iskcon_date = "".join(context.args)
            if DATE_PATTERN.fullmatch(iskcon_date):
                year, month = None, None
                for date in iskcon_date.split("-"):
                    if len(date) == 2:
                        month = int(date)
                    elif len(date) == 4:
                        year = int(date)

                if year and month:
                    body = f"# Iskcon events for {NUMBER_TO_MONTH[month]}-{year}\n"
                    events = self.get_iskcon_events([
                        NUMBER_TO_MONTH[month],
                        year
                    ], fetch_by="year&month")

                elif year:
                    body = f"# Iskcon events for {year}\n"
                    events = self.get_iskcon_events(year, fetch_by="year")

                elif month:
                    body = f"# Iskcon events for {month}-{2020}\n"
                    events = self.get_iskcon_events(NUMBER_TO_MONTH[month], fetch_by="month")

                for event in events:
                    body += f"\n## {event[1]}\n\n"
                    body += f"+ Year: {event[4]}\n"
                    body += f"+ Month: {event[2]}\n"
                    body += f"+ Day: {event[3]}\n"

                body_md_img = md_to_img(body)

                context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=body_md_img)
            
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Make sure to enter a valid date")            


    def get_ekadasi_events(self, data, fetch_by):
        with sqlite3.connect("data/vaishnadb.db") as conn:
            cursor = conn.cursor()
            if fetch_by == "year":
                cursor.execute("SELECT * FROM ekadasi_dates WHERE year=?", (data,))
            elif fetch_by == "month":
                cursor.execute("SELECT * FROM ekadasi_dates WHERE month=?", (data, ))
            elif fetch_by == "month&year":
                cursor.execute("SELECT * FROM ekadasi_dates WHERE month=? AND year=?", (data[0], data[1]))
            events = cursor.fetchall()
            return events


    def get_iskcon_events(self, data, fetch_by):
        with sqlite3.connect("data/vaishnadb.db") as conn:
            cursor = conn.cursor()
            if fetch_by == "year":
                cursor.execute("SELECT * FROM iskcon_events WHERE year=?", (data,))
            elif fetch_by == "month":
                cursor.execute("SELECT * FROM iskcon_events WHERE month=?", (data,))
            elif fetch_by == "month&year":
                cursor.execute("SELECT * FROM iskcon_events WHERE month=? AND year=?", (data[0], data[1]))
            events = cursor.fetchall()
            return events


    def get_ekadasi_events_from_file(self):
        with open("data/ekadasi.csv", "r") as csvfile:
           events = [ event for event in csv.reader(csvfile, delimiter=",") ]
        return events


    def get_iskcon_events_from_file(self):
        with open("data/iskcon_events.csv", "r") as csvfile:
            events = [ event for event in csv.reader(csvfile, delimiter=",") ]
        return events