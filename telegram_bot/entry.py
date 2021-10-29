from os import stat
import telegram
import subprocess
import os
import shlex
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot.util import build_menu, ocr_dict, pdf_dict, dash_dict, states_map
from telegram_bot.ocr_functions import ocr1, ocr2, pdf, dashboard, ka_detail, run_scraper
import json
import logging
import pdb

SENTINEL = dict()

def entry(bot, update):
    print(update)
    # MESSAGE & Is a REPLY
    if update.message and update.message.reply_to_message:
        try:
            if update.message.document.mime_type == 'application/pdf':
                pdf_file = update.message.document.get_file()
                print('>>>>>>>>>>>>>>', pdf_file)
                print(SENTINEL)
            return
        except Exception as e:
            logging.error(e)

    elif update.message:
        # CMD /help, /test, /start
        if update.message.text.startswith("/test"):
            update.message.reply_text("200 OK!", parse_mode=telegram.ParseMode.MARKDOWN)
            return

        # /start - List of states & returns the state ID
        if update.message.text.startswith("/start"):
            button_list = []
            for st_name in states_map.keys():
                button_list.append(
                    InlineKeyboardButton(
                        st_name, callback_data=states_map[st_name]
                    )
                )
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
            bot.send_message(
                chat_id=update.message.chat.id,
                text="Which state do you want to fetch data for?",
                reply_to_message_id=update.message.message_id,
                reply_markup=reply_markup,
            )
            return

        if update.message.text.startswith("/help"):
            help_text = f"""
            \n*OCR*
            - Send the bulletin image to do OCR
            - Errors and the results would be returned
            - If there are errors, copy the extracted text and make corrections.
            - Send it back to the text
            - Reply to the message with `/ocr2 "Madhya Pradesh"`
            \n*PDF*
            - Send the URL of the pdf bulletin
            - Choose the state. Default page number is 2.
            - For using different page number, use the command like below
            - `/pdf "Punjab" 3`
            \n*DASHBOARD*
            - `/dashboard`
            - Choose the state
            \n\n_Send `/test` for checking if the bot is online_"""

            update.message.reply_text(
                str(help_text), parse_mode=telegram.ParseMode.MARKDOWN
            )
            return

    # CALLBACK - Select a State ID
    if update.callback_query:
        # get state name
        STATE = update.callback_query.data
        SENTINEL['state'] = STATE

        bot.send_message(
            chat_id=update.callback_query.message.chat.id,
            text=f"Upload PDF for {STATE}"
        )


        # if update.callback_query.message.reply_to_message.text == "HR":
        #     bot.send_chat_action(
        #             chat_id=update.message.chat.id, action=telegram.ChatAction.TYPING
        #         )
        #     text_prev = update.message.text
        #     text_replaced = text_prev.replace("“", '"').replace("”", '"')
        #     text = shlex.split(text_replaced)
        #     try:
        #         if update.message.reply_to_message.document.mime_type == 'application/pdf':
        #             pdf_file = update.message.reply_to_message.document.get_file()
        #             ka_detail(bot,update.message.chat.id, pdf_file, text[1],text[2],text[3])
        #             return
        #     except Exception as e:
        #         logging.error(e)


def _entry(bot, update):
    print(update)
    print('------------------------------')
    pdb.set_trace()

    # try:
    #     # res = bot.send_message(chat_id="-1001429652488", text=update.to_json())
    #     # print(json.dumps(update.to_dict(), indent=2))
    #     pass
    # except Exception as e:
    #     logging.error(e)
    #     bot.send_message(chat_id="-1001429652488", text=str(e))
    #     pass


    if update.callback_query:

        # try:
        #     print('MMM<M<M<<M<M<MM<M', update)
        #     if update.message.document.mime_type == 'application/pdf':
        #         pdf_file = update.message.reply_to_message.document.get_file()
        #         print('we got a PDF fiule', state_code)
        #         return
        # except:
        #     pass

        if update.callback_query.message.reply_to_message.text == "HR":
            print('you got a reply to HR')

        if update.callback_query.message.reply_to_message.text == "/start":
            state_name = update.callback_query.data
            print('>>>>>>>>>', update)
            try:
                print('selected state', state_name)
                # if state_name == 'HR':
                bot.send_message(
                    chat_id=update.callback_query.message.chat.id,
                    text="upload pdf",
                    reply_to_message_id=update.callback_query.message.id
                    # reply_markup='this is a pdf, provide a pdf please',
                )

                # if states in pdf states
                #   reply back and ask for file
                # if states in image states
                #   reply back and ask for iamge
                # if this is an image
                #   run scrpaers.py --state_code & send back that image delta
                # if this is an pdf
                #   run scrpaers.py --state_code & send back that pdf delta

                # run_scraper(bot, update.callback_query.message.chat.id, state_name)
            except Exception as e:
                print('some error bro')
                # bot.send_message(
                #     chat_id=update.callback_query.message.chat.id,
                #     text="Dash fetch failed",
                # )
                # logging.error(e)

            return


        # If an image has been provided on chat
        # if update.callback_query.message.reply_to_message.photo:
        #     state_name = update.callback_query.data
        #     photo = update.callback_query.message.reply_to_message.photo[-1]
        #     is_translation_req = False
        #     start_end_districts = "auto,auto"

        #     if (
        #         state_name == "Bihar"
        #         or state_name == "Uttar Pradesh"
        #         or state_name == "Chhattisgarh"
        #     ):
        #         is_translation_req = True

        #     if(state_name == "Arunachal Pradesh"):
        #         start_end_districts = "Anjaw"

        #     if(state_name == "Tamil Nadu"):
        #         start_end_districts = "Ariyalur,Railway"

        #     if(state_name == "Meghalaya"):
        #         start_end_districts = "East,auto"

        #     ocr1(
        #         bot,
        #         update.callback_query.message.chat.id,
        #         photo,
        #         state_name,
        #         start_end_districts,
        #         is_translation_req,
        #     )

        # If user texted `/url` on chat
        # elif update.callback_query.message.reply_to_message.entities[0].type == "url":
        #     state_name = update.callback_query.data
        #     url = update.callback_query.message.reply_to_message.text
        #     page_num = 2

        #     try:
        #         pdf(
        #             bot,
        #             update.callback_query.message.chat.id,
        #             state_name,
        #             url,
        #             page_num,
        #         )
        #     except Exception as e:
        #         bot.send_message(
        #             chat_id=update.callback_query.message.chat.id,
        #             text="PDF extraction failed",
        #         )
        #         logging.error(e)

        # If user texted `/dashboard` on chat
        # elif update.callback_query.message.reply_to_message.text == "/dashboard":
        #     state_name = update.callback_query.data
        #     try:
        #         dashboard(bot, update.callback_query.message.chat.id, state_name)
        #     except Exception as e:
        #         bot.send_message(
        #             chat_id=update.callback_query.message.chat.id,
        #             text="Dash fetch failed",
        #         )
        #         logging.error(e)

        #     return

    # check if direct message
    if update.message:
        if update.message.text.startswith("/test"):
            update.message.reply_text("200 OK!", parse_mode=telegram.ParseMode.MARKDOWN)
            return

        if update.message.text.startswith("/start"):
            button_list = []
            for st_name in states_map.keys():
                button_list.append(
                    InlineKeyboardButton(
                        st_name, callback_data=states_map[st_name]
                    )
                )
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
            bot.send_message(
                chat_id=update.message.chat.id,
                text="Which state do you want to fetch data for?",
                reply_to_message_id=update.message.message_id,
                reply_markup=reply_markup,
            )
            return

        if update.message.text.startswith("/help"):
            help_text = f"""
            \n*Steps on how to run the bot to fetch data from state bulletins*
            1 `/start` will start the data fetching process
            2 Choose a state you want to enter data for
            3 Follow instructions to upload image or a PDF or call the dashboard url
            4 Copy & paste the output difference that needs to be entered in excel sheet
            \n\n_Send `/test` for checking if the bot is online_"""

            update.message.reply_text(
                str(help_text), parse_mode=telegram.ParseMode.MARKDOWN
            )
            return
        # Reply to the message
        # if update.message.photo:
        #     button_list = []
        #     for key in ocr_dict:
        #         button_list.append(
        #             InlineKeyboardButton(ocr_dict[key], callback_data=ocr_dict[key])
        #         )
        #     reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
        #     bot.send_message(
        #         chat_id=update.message.chat.id,
        #         text="Which state bulletin is this?",
        #         reply_to_message_id=update.message.message_id,
        #         reply_markup=reply_markup,
        #     )
        #     return

        # try:
        #     if update.message.entities[0].type == "url":
        #         button_list = []
        #         for key in pdf_dict:
        #             button_list.append(
        #                 InlineKeyboardButton(pdf_dict[key], callback_data=pdf_dict[key])
        #             )
        #         reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
        #         bot.send_message(
        #             chat_id=update.message.chat.id,
        #             text="""Which state's PDF bulletin is this?\n\nNote that default page number used is 2. If a different page number needs to be used, say 3 for WB bulletin, reply to the URL message you sent with : /pdf "West Bengal" 3""",
        #             reply_to_message_id=update.message.message_id,
        #             reply_markup=reply_markup,
        #         )
        #         return
        # except IndexError:
        #     return

        # try:
        #     if update.message.text.startswith("/dashboard"):
        #         bot.send_chat_action(
        #             chat_id=update.message.chat.id, action=telegram.ChatAction.TYPING
        #         )
        #         button_list = []
        #         print(dash_dict[key])
        #         for key in dash_dict:
        #             button_list.append(
        #                 InlineKeyboardButton(
        #                     dash_dict[key], callback_data=dash_dict[key]
        #                 )
        #             )
        #         reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
        #         bot.send_message(
        #             chat_id=update.message.chat.id,
        #             text="Which state's dashboard do you want to fetch?",
        #             reply_to_message_id=update.message.message_id,
        #             reply_markup=reply_markup,
        #         )
        #         return
        # except Exception as e:
        #     logging.error(e)
        #     bot.send_message(
        #         chat_id=update.message.chat.id, text="Something wrong.. :/"
        #     )
        #     return

        # if update.message.reply_to_message and update.message.text.startswith("/"):
        #     bot.send_chat_action(
        #         chat_id=update.message.chat.id, action=telegram.ChatAction.TYPING
        #     )
        #     text_prev = update.message.text
        #     text_replaced = text_prev.replace("“", '"').replace("”", '"')
        #     # Wrong input might cause the script to fail
        #     try:
        #         text = shlex.split(text_replaced)
        #     except Exception as e:
        #         bot.send_message(
        #             chat_id=update.message.chat.id,
        #             text="Wrong command?",
        #             reply_to_message_id=update.message.message_id,
        #         )
        #         return

        #     if update.message.text.startswith("/ocr1"):
        #         if len(text) < 4:
        #             return
        #         photo = update.message.reply_to_message.photo[-1]
        #         ocr1(bot, update.message.chat.id, photo, text[1], text[2], text[3])
        #     elif update.message.text.startswith("/ocr2"):
        #         if len(text) < 2:
        #             return
        #         ocr2(
        #             bot,
        #             update.message.chat.id,
        #             update.message.reply_to_message.text,
        #             text[1],
        #         )
        #     elif update.message.text.startswith("/pdf"):
        #         bot.send_chat_action(
        #             chat_id=update.message.chat.id, action=telegram.ChatAction.TYPING
        #         )
        #         text_prev = update.message.text
        #         text_replaced = text_prev.replace("“", '"').replace("”", '"')
        #         text = shlex.split(text_replaced)
        #         try:
        #             if update.message.reply_to_message.document.mime_type == 'application/pdf':
        #                 pdf_file = update.message.reply_to_message.document.get_file()
        #                 ka_detail(bot,update.message.chat.id, pdf_file, text[1],text[2],text[3])
        #                 return
        #         except Exception as e:
        #             logging.error(e)
        #         try:
        #             if update.message.reply_to_message.entities[0].type == "url":
        #                 url = update.message.reply_to_message.text
        #                 try:
        #                     pdf(bot, update.message.chat.id, text[1], url, text[2])
        #                 except Exception as e:
        #                     update.message.reply_text(
        #                         str(
        #                             """Reply to the pdf URL with\n`/pdf <state name> <page number>`"""
        #                         ),
        #                         parse_mode=telegram.ParseMode.MARKDOWN,
        #                     )
        #                     logging.error(e)
        #                     return
        #         except Exception as e:
        #             logging.error(e)
        #             return
        #     elif update.message.text.startswith("/test"):
        #         message = "200 OK!"
        #         return



