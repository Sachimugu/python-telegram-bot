### Python Telegram Bot

# Telegram Bot for Group Management and Communication

This project is a Telegram bot that allows users to manage multiple groups and channels, assign categories to them, send messages/photos to groups, and apply filters to specific commands/messages. The bot supports both private and group interactions and enables efficient communication with different categories of groups.

## Features

1. **Group Management**: 
    - Register groups by their `Chat ID` and `Group Name`.
    - Assign categories to groups for better organization.
    - Display groups based on categories.
    - Delete or modify group categories.

2. **Message and Photo Broadcasting**:
    - Send text messages or photos to all groups or groups under specific categories.
    - Send messages/photos with hyperlinks (converted from markdown links).
    
3. **Filters**:
    - Add filters to group commands (e.g., `/info` triggers a specific response for groups in the same category).
    - Configure custom responses based on predefined filters for commands.

4. **Category and Filter Management**:
    - Set categories for groups.
    - View or delete groups’ assigned categories.
    - Add or modify filters for different categories and commands.

## Setup

### Prerequisites

- Python 3.x
- Required Python libraries: `python-telegram-bot`, `pandas`, and `os`.

You can install the necessary dependencies using pip:

```bash
pip install python-telegram-bot pandas
