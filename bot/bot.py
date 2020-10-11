import os
import csv
import sqlite3
import logging
import telegram
from datetime import datetime
from dotenv import load_dotenv
from helpers.beautify import beautify_to_pdf
from helpers.vaishnadb import VaishnaDB
from helpers.helpers import DATE_PATTERN, NUMBER_TO_MONTH, events_to_dict
from telegram.parsemode import ParseMode
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters



logging.basicConfig(
    filename="logs.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


log_handler = logging.StreamHandler(os.sys.stdout)
log_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)    



class VaishnaBot():
    load_dotenv()
    def __init__(self):

        self.logger = logging.getLogger(name="vaishnabot")
        self.logger.addFilter(log_handler)
        
        self.vaishnadb = VaishnaDB()

        self.updater = Updater(token=os.getenv("BOTKEY"), use_context=True)
        
        self.updater.dispatcher.add_handler(CommandHandler("start", self.start))
        self.updater.dispatcher.add_handler(CommandHandler("help", self.help))
        self.updater.dispatcher.add_handler(CommandHandler("ekadasi", self.ekadasi_event))
        self.updater.dispatcher.add_handler(CommandHandler("iskcon_events", self.iskcon_event))
        self.updater.dispatcher.add_handler(CommandHandler("remindme", self.remindme))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.message_handler))

        self.botkey = os.getenv("BOTKEY")

        self.updater.start_polling()

        print("Vaishnabot initialized!")

        self.updater.idle()
        

    def start(self, update, context):
        username = update.message.chat.username
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello {username}! Hare Krishna! I'm Vaishnabot, you can know more about me running the /help command")

    
    def help(self, update, context):
        text = """Hi I'm Vaishnabot. You can send me commands to receive events and to remind you about them one day before.

        The commands you can send me are:

        * Events

        /ekadasi <args>
        /iskcon_events <args>

        Where args: <mm>, <YYYY>, <mm>-<YYYY>, <YYYY>-<mm>

        * Reminder

        /remindme <args>
        
        Where args: <ekadasi>, <iskcon_events>
        """
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)


    def message_handler(self, update, context):
        username = update.message.chat.username
        human_said = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"You {username} said: {human_said}")


    @staticmethod
    def callback_ekadasi(context):
        """
            Get the ekadasi date for the current month starting from the day the function
            was called. The interval gets updated to next event one dat be4 it starts. 
        """
        username = update.message.chat.username
        ekadasi_name = "Krishna"
        starts = "08:20 AM"
        ends = "12:12 PM"

        text = f"""
        Hello {username}! just to remmind you that tomorrow's ekadasi {ekadasi_name}, so you must be prepared.
        It starts from {starts} to {ends}.
        """

        job = context.job
        print(job.interval)
        print(job)

        context.bot.send_message(chat_id=update.effective_chat.id, text=text)


    @staticmethod
    def callback_iskcon_events(context):
        text = "Reminder for Iskcon events"
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)


    def remindme(self, update, context):
        if not context.args:
            text = """
            I can remind you about events one day before they start so you can be prepared! Just tell me which events of the following you'd like to be reminded:

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
                    args = "".join(context.args)
                    if args == "iskcon_events":
                        print("iskcon events reminder")
                        iskcon_events_job = self.updater.job_queue.run_repeating(callback_iskcon_events, interval=1)
                    elif args == "ekadasi":
                        print("ekadasi reminder")
                        ekadasi_job = self.updater.job_queue.run_repeating(callback_ekadasi, interval=10)
                    elif args == "cancel":
                        pass
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"I will remind you about {args} one day after it starts so you can be prepared")

                
    def ekadasi_event(self, update, context):
        self.logger.info("User {} requested /ekadasi command".format(update.message.chat.username))
                
        if not context.args: 
            context.bot.send_message(chat_id=update.effective_chat.id, text="I'll show you the Ekadasi dates for this year")
            current_year = str(datetime.today().year)
            events = self.vaishnadb.get_ekadasi_events(current_year, fetch_by="year")
            events_dict = events_to_dict(events, kind="ekadasi")

            data = {
                "events": events_dict,
                "year": current_year,
                "month": ""
            }

            pdf_encoded_bytes = beautify_to_pdf(data, kind="ekadasi")
            
            context.bot.sendDocument(chat_id=update.effective_chat.id, document=pdf_encoded_bytes, filename="ekadasi.pdf")

        else:
            args = "".join(context.args)

            data = {}
            
            if DATE_PATTERN.fullmatch(args):
                year, month = None, None

                for date in args.split("-"):
                    if len(date) == 2:
                        month = str(date)
                    elif len(date) == 1:
                        month = "0" + str(date)
                    elif len(date) == 4:
                        year = str(date)
                
                if year and month:
                    events = self.vaishnadb.get_ekadasi_events([year, month], fetch_by="month&year")

                elif year:
                    events = self.vaishnadb.get_ekadasi_events(year, fetch_by="year")

                elif month:
                    events = self.vaishnadb.get_ekadasi_events(month, fetch_by="month")
                

                if events:
                    events_dict = events_to_dict(events, kind="ekadasi")
                    data["events"] = events_dict

                    if not year:
                        data["year"] = str(datetime.today().year)
                    else:
                        data["year"] = year

                    try:
                        data["month"] = NUMBER_TO_MONTH[int(month)]
                    except:
                        data["month"] = ""
                
                    pdf_encoded_bytes = beautify_to_pdf(data, kind="ekadasi")
                    context.bot.sendDocument(chat_id=update.effective_chat.id, document=pdf_encoded_bytes, filename="ekadasi.pdf")

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
            events = self.vaishnadb.get_iskcon_events(current_year, fetch_by="year")
            
            events_dict = events_to_dict(events, kind="iskcon")
           
            data = {
                "events": events_dict,
                "year": current_year,
                "month": ""
            }

            pdf_encoded_bytes = beautify_to_pdf(data, kind="iskcon_events")

            context.bot.sendDocument(chat_id=update.effective_chat.id, document=pdf_encoded_bytes, filename="iskcon_events.pdf")

        else: 
            args = "".join(context.args)

            data = {}

            if DATE_PATTERN.fullmatch(args):
                year, month = None, None
                for date in args.split("-"):
                    if len(date) == 2:
                        month = str(date)
                    elif len(date) == 1:
                        month = "0" + str(date)
                    elif len(date) == 4:
                        year = str(date)

                if year and month:
                    events = self.vaishnadb.get_iskcon_events([year, month], fetch_by="month&year")

                elif year:
                    events = self.vaishnadb.get_iskcon_events(year, fetch_by="year")

                elif month:
                    events = self.vaishnadb.get_iskcon_events(month, fetch_by="month")

                if events:

                    events_dict = events_to_dict(events, kind="iskcon")
                    data["events"] = events_dict

                    if not year:
                        data["year"] = str(datetime.today().year)
                    else:
                        data["year"] = year

                    if not month:
                        data["month"] = ""
                    else:
                        data["month"] = NUMBER_TO_MONTH[int(month)]

                    pdf_encoded_bytes = beautify_to_pdf(data, kind="iskcon_events")
                    context.bot.sendDocument(chat_id=update.effective_chat.id, document=pdf_encoded_bytes, filename="iskcon_events.pdf")
            
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Make sure to enter a valid date")