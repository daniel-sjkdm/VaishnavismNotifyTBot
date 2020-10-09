import os
import csv
import sqlite3
import logging
import telegram
from datetime import datetime
from dotenv import load_dotenv
from helpers.vaishnadb import VaishnaDBPG
from helpers.helpers import DATE_PATTERN, NUMBER_TO_MONTH, html_to_pdf_v2
from telegram.parsemode import ParseMode
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters



logging.basicConfig(
    filename="logs.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


class VaishnaBot():
    def __init__(self):

        self.logger = logging.getLogger(name="vaishnabot")
        
        self.vaishnadb = VaishnaDBPG()

        self.updater = Updater(token=os.getenv("BOTKEY"), use_context=True)
        
        self.updater.dispatcher.add_handler(CommandHandler("start", self.start))
        self.updater.dispatcher.add_handler(CommandHandler("ekadasi", self.ekadasi_event))
        self.updater.dispatcher.add_handler(CommandHandler("iskcon_events", self.iskcon_event))
        self.updater.dispatcher.add_handler(CommandHandler("remindme", self.remindme))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.message_handler))

        self.botkey = os.getenv("BOTKEY")
        
        self.updater.start_webhook(listen="0.0.0.0",
                          port=os.getenv("PORT"),
                          url_path=self.botkey
        )

        self.updater.bot.setWebhook(f"https://vaishnabot.herokuapp.com/{self.botkey}")

        print("Vaishnabot initialized!")

        self.updater.idle()
        

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hari Bol! Hare Krishna! I'm Vaishnabot")


    def message_handler(self, update, context):
        username = update.message.chat.username 
        human_said = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"You {username} said: {human_said}")


    def remindme(self, update, context):
        if not context.args:
            text = """
                I can remind you about events one day before they start so you can be prepared!
                Just tell me which events of the following you'd like to be reminded:
                - iskcon events: /remindme iskcon_events
                - ekadasi: /remindme ekadasi
                - both: /remindme iskcon_events ekadasi
                You can also cancel the reminders:
                - /remindme cancel <event_name> 
            """
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)

        else:
            for arg in context.args:
                if arg not in ["iskcon_events", "ekadasi", "cancel"]:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Make sure to enter valid events!")
                else:
                    # add its respective job
                    pass 


    def ekadasi_event(self, update, context):
        self.logger.info("User {} requested /ekadasi command".format(update.message.chat.username))
                
        if not context.args: 
            context.bot.send_message(chat_id=update.effective_chat.id, text="I'll show you the Ekadasi dates for this year")
            current_year = str(datetime.today().year)

            body = "# Ekadasi dates for this year"

            events = self.vaishnadb.get_ekadasi_events(current_year, fetch_by="year")

            for event in events:
                body += f"\n## {event[1]}\n\n"
                body += f"Month: {event[3]}\n"
                body += f"Day: {event[2]}\n"
                body += f"Year: {event[4]}\n"
                body += f"Starts: {event[5]}\n"
                body += f"Ends: {events[6]}\n"
            
            body_pdf_encoded_bytes = html_to_pdf_v2(body)
            
            context.bot.sendDocument(chat_id=update.effective_chat.id, document=body_pdf_encoded_bytes, filename="ekadasi.pdf")

        else:
            args = "".join(context.args)
            if DATE_PATTERN.fullmatch(args):
                year, month = None, None

                for date in args.split("-"):
                    if len(date) == 2 or len(date) == 1:
                        month = NUMBER_TO_MONTH[int(date)]
                    elif len(date) == 4:
                        year = str(date)
                
                if year and month:
                    body = f"# Ekadasi events for {month}-{year}\n"
                    events = self.vaishnadb.get_ekadasi_events([month, year], fetch_by="month&year")

                elif year:
                    body = f"# Ekadasi events for {year}\n"
                    events = self.vaishnadb.get_ekadasi_events(year, fetch_by="year")

                elif month:
                    body = f"# Ekadasi events for {month}\n"
                    events = self.vaishnadb.get_ekadasi_events(month, fetch_by="month")
                
                for event in events:
                    body += f"\n## {event[1]}\n\n"
                    body += f"Month: {event[3]}\n"
                    body += f"Day: {event[2]}\n"
                    body += f"Year: {event[4]}\n"
                    body += f"Starts: {event[5]}\n"
                    body += f"Ends: {event[6]}\n"

                body_pdf_encoded_bytes = html_to_pdf_v2(body)

                context.bot.sendDocument(chat_id=update.effective_chat.id, document=body_pdf_encoded_bytes, filename="ekadasi.pdf")

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
            current_year = str(datetime.today().year)
            body = f"# Iskcon {current_year} events\n"
            events = self.vaishnadb.get_iskcon_events(str(current_year), fetch_by="year")
            
            for event in events:
                body += f"\n## {event[1]}\n\n"
                body += f"+ Year: {event[4]}\n"
                body += f"+ Month: {event[2]}\n"
                body += f"+ Day: {event[3]}\n"
            
            body_pdf_encoded_bytes = html_to_pdf_v2(body)

            context.bot.sendDocument(chat_id=update.effective_chat.id, document=body_pdf_encoded_bytes, filename="iskcon_events.pdf")

        else: 
            args = "".join(context.args)
            if DATE_PATTERN.fullmatch(args):
                year, month = None, None
                for date in args.split("-"):
                    if len(date) == 2 or len(date) == 1:
                        month = NUMBER_TO_MONTH[int(date)]
                    elif len(date) == 4:
                        year = date

                if year and month:
                    body = f"# Iskcon events for {month}-{year}\n"
                    events = self.vaishnadb.get_iskcon_events([month, year], fetch_by="month&year")

                elif year:
                    body = f"# Iskcon events for {year}\n"
                    events = self.vaishnadb.get_iskcon_events(year, fetch_by="year")

                elif month:
                    body = f"# Iskcon events for {month}-{2020}\n"
                    events = self.vaishnadb.get_iskcon_events(month, fetch_by="month")

                for event in events:
                    body += f"\n## {event[1]}\n\n"
                    body += f"+ Year: {event[4]}\n"
                    body += f"+ Month: {event[2]}\n"
                    body += f"+ Day: {event[3]}\n"

                body_pdf_encoded_bytes = html_to_pdf_v2(body)

                context.bot.sendDocument(chat_id=update.effective_chat.id, document=body_pdf_encoded_bytes, filename="iskon_events.pdf")
            
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Make sure to enter a valid date")