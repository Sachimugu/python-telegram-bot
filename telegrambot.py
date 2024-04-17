import re
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
import logging
import pandas as pd
from telegram.ext import CallbackContext
import os
import traceback

API_TOKEN = '6519283028:AAGYGdyXVpVaHI6-tLAT72rECJvjbZVpn3Y'

# Replace 'YOUR_BOT_ID' with your actual bot's user ID
BOT_ID = "1664999734"
updater = Updater(token=API_TOKEN)
dispatcher = updater.dispatcher

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)




def get_channel_group_ids(update, context):
    chat_id = update.message.chat.id
    chat_type = update.message.chat.type
    group_name = update.message.chat.title
    message_text = update.message.text  # Get the group name

    if chat_type != 'private':
        if message_text.startswith('/'):
            track_and_respond(message_text, chat_id, context)
 
            print(f"Message from group {chat_id}: {message_text}") 
# register group id for mesage
        existing_df = pd.DataFrame({'Chat ID': [chat_id], 'Group Name': [group_name], 'Type': [chat_type], 'Category': ['']})
        if not os.path.isfile('channel_group_ids.csv'):
            existing_df.to_csv('channel_group_ids.csv', mode='a', index=False, header=True)  # Add header if file doesn't exist
        else:
            existing_df.to_csv('channel_group_ids.csv', mode='a', index=False, header=False)  # Append without header
        df = pd.read_csv('channel_group_ids.csv')
        df_no_duplicates = df.drop_duplicates(subset=['Chat ID'])
        df_no_duplicates.to_csv('channel_group_ids.csv', index=False)  # Save without header

# Message handler to trigger the function when a message is sent to any group
message_handler = MessageHandler(Filters.text & (Filters.chat_type.groups | Filters.chat_type.supergroup), get_channel_group_ids)
dispatcher.add_handler(message_handler)

def print_group_messages(update, context):
    if update.message.chat.type != 'private':
        message_text = update.message.text
        chat_id = update.message.chat.id
        print(f"Message from group {chat_id}: {message_text}")

# Message handler to trigger the function when a message is sent to any group
print_group_message_handler = MessageHandler(Filters.text & (Filters.chat_type.groups | Filters.chat_type.supergroup), print_group_messages)
dispatcher.add_handler(print_group_message_handler)



def convert_links_to_hyperlinks(text):
    if text:
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        def replace_link(match):
            text = match.group(1)
            url = match.group(2)
            return f'<a href="{url}">{text}</a>'
        return re.sub(link_pattern, replace_link, text)
    else:
        return None
    

def send_photo_to_groups(update, context):
    user_id = update.effective_user.id
    df = pd.read_csv('channel_group_ids.csv')
    group_chat_ids = set(df['Chat ID'].tolist())

    if user_id == bot_creator_id:
        photo = update.message.photo[-1].file_id
        caption = update.message.caption

        if caption:
            for chat_id in group_chat_ids:
                context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
        else:
            for chat_id in group_chat_ids:
                context.bot.send_photo(chat_id=chat_id, photo=photo)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")
        

def send_message_to_groups(update, context):
    df = pd.read_csv('channel_group_ids.csv')
    group_chat_ids = set(df['Chat ID'].tolist())
    # print (group_chat_ids)
    # print ('group_chat_ids')
    user_id = update.effective_user.id

    if user_id == bot_creator_id:
        message = update.message.text
        caption = update.message.caption

        # Check for links in message or caption
        message = convert_links_to_hyperlinks(message)
        caption = convert_links_to_hyperlinks(caption)

        for chat_id in group_chat_ids:
            if update.message.photo:  # Send photo with caption (if any)
                context.bot.send_photo(chat_id=chat_id, photo=update.message.photo[-1].file_id, caption=caption, parse_mode='HTML')
            elif message:  # Send text message if it exists
                context.bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
        context.bot.send_message(chat_id=update.effective_chat.id, text="message sent to all categories")

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")


# Function to send photo to multiple groups
def send_photo_to_groups(update, context):
    df = pd.read_csv('channel_group_ids.csv')
    group_chat_ids = set(df['Chat ID'].tolist())
    # print (group_chat_ids)
    # print ('group_chat_ids')
    user_id = update.effective_user.id

    if user_id == bot_creator_id:
        photo = update.message.photo[-1].file_id
        caption = update.message.caption  # Get caption from message
        if caption:  # Check if caption exists
            for chat_id in group_chat_ids:
                context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
        else:
            for chat_id in group_chat_ids:
                context.bot.send_photo(chat_id=chat_id, photo=photo)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Image and photos sent to all categories")
    
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")


def send_message_to_groups_with_category(update, context, category):
    df = pd.read_csv('channel_group_ids.csv')
    group_chat_ids = df[df['Category'] == category]['Chat ID'].tolist()
    # print (group_chat_ids)
    user_id = update.effective_user.id

    if user_id == bot_creator_id:
        message = update.message.text
        caption = update.message.caption

        # Check for links in message or caption
        message = convert_links_to_hyperlinks(message)
        caption = convert_links_to_hyperlinks(caption)

        for chat_id in group_chat_ids:
            if update.message.photo:  # Send photo with caption (if any)
                context.bot.send_photo(chat_id=chat_id, photo=update.message.photo[-1].file_id, caption=caption, parse_mode='HTML')
            elif message:  # Send text message if it exists
                context.bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Message sent to {category}.")

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")


# Function to send photo to multiple groups
def send_photo_to_groups_with_category(update, context, category):
    df = pd.read_csv('channel_group_ids.csv')
    group_chat_ids = df[df['Category'] == category]['Chat ID'].tolist()
    # print (group_chat_ids)
    user_id = update.effective_user.id

    if user_id == bot_creator_id:
        photo = update.message.photo[-1].file_id
        caption = update.message.caption  # Get caption from message
        if caption:  # Check if caption exists
            for chat_id in group_chat_ids:
                context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
        else:
            for chat_id in group_chat_ids:
                context.bot.send_photo(chat_id=chat_id, photo=photo)
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Image and message sent to {category}.")

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")


def message_handler(update, context):
    message = update.message.text
    caption = update.message.caption
    # print('\ncontext.user_data')
    # print(context.user_data)
    if context.user_data:

        if 'selected_category' in context.user_data:
            category = context.user_data['selected_category']
            if category == 'All':
                send_message_to_groups(update, context)
                del context.user_data['selected_category'] 
            else:
                send_message_to_groups_with_category(update, context, category)
                del context.user_data['selected_category'] 
        else:
            # Handle the case where the user sends a message without selecting a category first
            update.message.reply_text("Please select a category first.")
        # Clear the selected_category key from context.user_data
        # del context.user_data['selected_category']
conversation_handler = MessageHandler(Filters.text & ~Filters.command, message_handler)
dispatcher.add_handler(conversation_handler)


def photo_handler(update, context):
    message = update.message.text
    caption = update.message.caption
    # print('\ncontext.user_data')
    # print(context.user_data)
    if context.user_data:
        if 'selected_category' in context.user_data:
            category = context.user_data['selected_category']
            if category == 'All':
                send_photo_to_groups(update, context)
                del context.user_data['selected_category'] 
            else:
                send_photo_to_groups_with_category(update, context, category)
                del context.user_data['selected_category'] 
        else:
            # Handle the case where the user sends a message without selecting a category first
            update.message.reply_text("Please select a category first.")
        # del context.user_data['selected_category'] 

photo_handler = MessageHandler(Filters.photo & ~Filters.command, photo_handler)
dispatcher.add_handler(photo_handler)



def set_category(update, context):
    user_id = update.effective_user.id
    
    print('user_id: %s' % user_id)
    print(user_id)
    df = pd.read_csv('channel_group_ids.csv')
    # print(user_id)
    # print(bot_creator_id)
    

    if user_id == bot_creator_id:
        groups_without_categories = df[df['Category'].isnull() | (df['Category'] == '')]

        if not groups_without_categories.empty:
            group_names = groups_without_categories['Group Name'].tolist()
            # Generate buttons for groups dynamically
            group_buttons = [[InlineKeyboardButton(group_name, callback_data=f'group_{group_name}')] for group_name in group_names]
            reply_markup = InlineKeyboardMarkup(group_buttons)

            update.message.reply_text("Please select a group to set its category:", reply_markup=reply_markup)
        else:
            update.message.reply_text("All groups already have categories assigned.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Register the command handler for setting categories
set_category_handler = CommandHandler('set_cat', set_category)
dispatcher.add_handler(set_category_handler)


def select_group(update, context):
    query = update.callback_query
    # print(query)
    group_name = query.data.split('_')[1]

    # Prepare keyboard for categories
    categories = ['Investors', 'Partners', 'KOLs', 'Unknown1', 'Unknown2', 'Unknown3']
    category_buttons = [[InlineKeyboardButton(category, callback_data=f'category_{category}_{group_name}')] for category in categories]
    reply_markup = InlineKeyboardMarkup(category_buttons)

    query.message.reply_text(f"Please select a category for {group_name}:", reply_markup=reply_markup)


def select_category(update, context):
    query = update.callback_query
    # print(query)
    category, group_name = query.data.split('_')[1:]

    df = pd.read_csv('channel_group_ids.csv')
    df.loc[df['Group Name'] == group_name.strip(), 'Category'] = category.strip()
    df.to_csv('channel_group_ids.csv', index=False)  # Save without header

    query.message.reply_text(f"Category for {group_name} set as {category}.")

# Register the callback handlers for group selection and category selection
dispatcher.add_handler(CallbackQueryHandler(select_group, pattern=r'^group_'))
dispatcher.add_handler(CallbackQueryHandler(select_category, pattern=r'^category_'))


def delete_group_category(update, context):
    user_id = update.effective_user.id
    df = pd.read_csv('channel_group_ids.csv')

    if user_id == bot_creator_id:
        # Filter out groups with categories assigned
        groups_with_categories = df[df['Category'].notnull()]

        if not groups_with_categories.empty:
            group_names = groups_with_categories['Group Name'].tolist()
            # Generate buttons for group selection dynamically
            group_buttons = [[InlineKeyboardButton(group_name, callback_data=f'delete_group_category_{group_name}')] for group_name in group_names]
            reply_markup = InlineKeyboardMarkup(group_buttons)

            update.message.reply_text("Please select a group to delete its category:", reply_markup=reply_markup)
        else:
            update.message.reply_text("No groups with categories found.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Register the command handler for deleting a group's category
delete_group_category_handler = CommandHandler('delete_cat', delete_group_category)
dispatcher.add_handler(delete_group_category_handler)


def confirm_delete_group_category(update, context):
    query = update.callback_query
    group_name = query.data.split('_')[-1]

    df = pd.read_csv('channel_group_ids.csv')
    if group_name in df['Group Name'].tolist():
        df.loc[df['Group Name'] == group_name, 'Category'] = ''  # Set the category to empty for the selected group
        df.to_csv('channel_group_ids.csv', index=False)  # Save the updated DataFrame back to the CSV file

        query.message.reply_text(f"Category for {group_name} deleted successfully.")
    else:
        query.message.reply_text(f"Group {group_name} not found.")

# Register the callback query handler for confirming group category deletion
delete_group_category_confirm_handler = CallbackQueryHandler(confirm_delete_group_category, pattern=r'^delete_group_category_')
dispatcher.add_handler(delete_group_category_confirm_handler)



def show_groups_in_category(update, context):
    user_id = update.effective_user.id
    df = pd.read_csv('channel_group_ids.csv')

    if user_id == bot_creator_id:
        unique_categories = df['Category'].dropna().unique()
        categories = unique_categories.tolist()
        # categories = ['Investors', 'Partners']  # Your list of categories
        if categories:
            # Create inline keyboard buttons for each category
            keyboard = [[InlineKeyboardButton(category, callback_data=f'show_groups_{category}')] for category in categories]
            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text("Please select a category display it groups:", reply_markup=reply_markup)
        else:
            update.message.reply_text("No categories found.")
    else:
        update.message.reply_text("You are not authorized to use this command.")

# Register the command handler for showing groups in a category
show_groups_in_category_handler = CommandHandler('groups_cat', show_groups_in_category)
dispatcher.add_handler(show_groups_in_category_handler)

def show_groups_for_category(update, context):
    query = update.callback_query
    # print(query.data)
    category = query.data.split('_')[-1]
    # print(category)

    df = pd.read_csv('channel_group_ids.csv')
    groups_in_category = df[df['Category'] == category]['Group Name'].tolist()
    # print(groups_in_category)

    if groups_in_category:
        message = f"Groups in category '{category}':\n\n"
        message += "\n".join(groups_in_category)
    else:
        message = f"No groups found in category '{category}'."

    query.message.reply_text(message)

# Register the callback query handler for showing groups in a category
show_groups_for_category_handler = CallbackQueryHandler(show_groups_for_category, pattern=r'^show_groups_')
dispatcher.add_handler(show_groups_for_category_handler)


# Dictionary to store temporary filter data
filter_data = {'Category': [], 'Command': [], 'Message': []}

# Function to handle /addfilter command
def add_filter(update, context):
    update.message.reply_text("Please enter the category, command, and message separated by commas to set filters.\n\ne.g\nInvestors, /info, A simple telegram bot ")
    return 'WAITING_INPUT'

# Function to handle user input
def get_filter_info(update, context, function_identifier):
    print(update.message.chat.type)
    print(function_identifier)
    if update.message.chat.type != 'private':
        # If the message is not sent privately, ignore it
        return
    
    if function_identifier == 1:
        user_input = update.message.text.strip()
        category, command, message = user_input.split(',')
        
        # Load existing data from filter.csv
        if os.path.exists('filter.csv'):
            filter_df = pd.read_csv('filter.csv')
        else:
            filter_df = pd.DataFrame(columns=['Category', 'Command', 'Message'])
        
        # Check if the combination of Command and Category already exists
        existing_index = (filter_df['Command'] == command.strip()) & (filter_df['Category'] == category.strip())
        if existing_index.any():  # If combination exists, update the message
            filter_df.loc[existing_index, 'Message'] = message.strip()
        else:  # If combination doesn't exist, append new data
            new_row = {'Category': category.strip(), 'Command': command.strip(), 'Message': message.strip()}
            new_row_df = pd.DataFrame([new_row])  # Create a DataFrame with the new row data
            filter_df = pd.concat([filter_df, new_row_df], ignore_index=True)  # Concatenate the new row DataFrame with the existing DataFrame
        
        # Write back to filter.csv
        filter_df.to_csv('filter.csv', index=False)
        
        update.message.reply_text("Filter added successfully.")
        return 'WAITING_INPUT'

# Define the conversation states
WAITING_INPUT = 1

# Add the command handler and message handler to the dispatcher
dispatcher.add_handler(CommandHandler('set_filters', add_filter))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda update, context: get_filter_info(update, context, function_identifier=1)), group=1)





def track_and_respond(message_text, chat_id, context):
    print("track_and_respond")
    print(message_text)
    
    # Load the filter and channel_group_ids CSV files
    filter_df = pd.read_csv('filter.csv')
    cddf = pd.read_csv('channel_group_ids.csv')
    
    if message_text.strip() == '/filters':
        # Find the category of the chat_id
        filtered_df = cddf[cddf['Chat ID'] == chat_id]
        if not filtered_df.empty:
            category = filtered_df.iloc[0]['Category']
            
            # Send all filter commands with the same category
            commands_to_send = filter_df[filter_df['Category'] == category]['Command'].tolist()
            response_message = "\n".join(commands_to_send)
            context.bot.send_message(chat_id=chat_id, text=response_message)
    else:
        # Check if the message contains any commands from the filter
        for _, row in filter_df.iterrows():
            if row['Command'].lower() in message_text.lower():
                # Find the category of the chat_id
                filtered_df = cddf[cddf['Chat ID'] == chat_id]
                if not filtered_df.empty:
                    category = filtered_df.iloc[0]['Category']
                    
                    # Check if the command category matches the chat's category
                    if row['Category'] == category:
                        response_message = row['Message']
                        context.bot.send_message(chat_id=chat_id, text=response_message)
                        break



def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Send Message", callback_data='send_message')],
        [InlineKeyboardButton("Send Image and Message", callback_data='send_photo')],
        [InlineKeyboardButton("More Commands", callback_data='more_commands')],
        # [InlineKeyboardButton("List Groups without Categories", callback_data='list_groups')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose an action:', reply_markup=reply_markup)#11

def button(update, context):
    query = update.callback_query
    query.answer()

    action = query.data

    df = pd.read_csv('channel_group_ids.csv')
    unique_categories = df['Category'].dropna().unique()
    categories = ['All'] + unique_categories.tolist()

    if action == 'send_message':


         
        category_buttons = [[InlineKeyboardButton(category, callback_data=f'send_message_{category}')] for category in categories]
        reply_markup = InlineKeyboardMarkup(category_buttons)

        query.message.reply_text("Please select a category to send message to:", reply_markup=reply_markup)
    elif action.startswith('send_message'):
        _, _, category = action.split('_')
        context.user_data['selected_category'] = category  # Store selected category in user_data
        query.message.reply_text(f"Please enter the message for {category} category")
    elif action == 'send_photo':
        # categories = ['All', 'Investors', 'Partners']
        category_buttons = [[InlineKeyboardButton(category, callback_data=f'send_photo_{category}')] for category in categories]
        reply_markup = InlineKeyboardMarkup(category_buttons)

        query.message.reply_text("Please select a category to Image and message to:", reply_markup=reply_markup)
    elif action.startswith('send_photo'):
        _, _, category = action.split('_')
        context.user_data['selected_category'] = category  # Store selected category in user_data
        query.message.reply_text(f"Select image and message for {category} category")
    elif action == 'more_commands':
        query.message.reply_text(""" Click command\n\n/set_cat to set the category\n\n/delete_cat to delete group's category\n\n/groups_cat to view group category\n\n/set_filters to set group filter\n
        """)



start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

button_handler = CallbackQueryHandler(button)
dispatcher.add_handler(button_handler)




def error(update, context):
    # Log the error message
    logging.error('Update "%s" caused error "%s"', update, context.error)
    
    # Log traceback information
    traceback_str = traceback.format_exc()
    logging.error(traceback_str)

dispatcher.add_error_handler(error)

bot_creator_id = int(BOT_ID)

updater.start_polling()
print("Bot is running...")
updater.idle()