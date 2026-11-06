# Telegram bot Python and chat automation bot for Google Maps

This chat automation bot queries Google Maps via RapidAPI and returns structured Excel spreadsheets to Telegram users.

This repository contains a Telegram bot Python implementation for chat automation bot workflows. The application listens for search queries sent in Telegram, retrieves location records from RapidAPI, and sends formatted Excel spreadsheets back to the user.

Developers seeking python-telegram-bot patterns for chat automation can run this bot to gather business information such as phone numbers, ratings, review counts, and physical addresses.

## Architecture

The system has two Python source files:

- `telegram_bot.py`: The entry point for the application. It creates a `telebot.TeleBot` instance using the `bot_token` environment variable, registers message handlers, and runs the event loop with `bot.infinity_polling()`.
- `map_data.py`: The data retrieval and file export module. It queries the RapidAPI Google Maps endpoint, formats the returned data into a pandas `DataFrame`, and saves the table to an `.xlsx` workbook.

The runtime flow proceeds in five steps:

1. A user sends a text message containing search terms to the bot.
2. The `echo_all` handler in `telegram_bot.py` sends an immediate status reply: "Processing your results...".
3. The handler passes the search query to `main(loc)` in `map_data.py`.
4. `map_data.py` issues a GET request to `https://maps-data.p.rapidapi.com/searchmaps.php` with the query string parameter `query`. It parses the JSON payload, extracts business fields, builds a table with pandas, and writes `{loc}.xlsx` to the filesystem.
5. `telegram_bot.py` sends a confirmation message ("Your Results Processed."), uploads the Excel file to the chat via `bot.send_document`, and deletes the local file with `os.remove`.

## Setup

### Prerequisites

- Python 3.8 or higher
- Telegram bot token from @BotFather
- RapidAPI account with access to the Google Maps searchmaps endpoint

### Installation

1. Clone the repository:
```bash
git clone https://github.com/devsanthoshmk/telegtram-bot.git
cd telegtram-bot
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install pyTelegramBotAPI requests pandas openpyxl
```

## Usage

1. Export the Telegram bot token:
```bash
export bot_token="your_telegram_bot_token"
```

2. Run the bot script:
```bash
python telegram_bot.py
```

3. Send commands and queries in Telegram:
- Send `/start` or `/hello` to view the greeting message.
- Send any location or business query (for example, `coffee shop in Seattle`) to receive the generated Excel workbook.

## Configuration

The bot uses the following settings:

| Name | Type | Source | Description |
| :--- | :--- | :--- | :--- |
| `bot_token` | String | Environment variable (`os.environ.get('bot_token')`) | Telegram API authentication token |
| `X-RapidAPI-Key` | String | Hardcoded in `map_data.py` | RapidAPI API key for maps-data requests |
| `X-RapidAPI-Host` | String | Hardcoded in `map_data.py` | RapidAPI host header set to `maps-data.p.rapidapi.com` |

The exported Excel file contains eight columns:

- `NAME`: Name of the business or place
- `TYPE`: Comma-separated category types
- `STATUS`: Operation state (`Functioning`, `Not Sure`, or empty)
- `RATING`: Numerical review rating
- `REVIEW_COUNT`: Number of published reviews
- `PHONE NO.`: Listed telephone number
- `ADDRESS`: Full street address
- `LINKS`: Excel hyperlink formula linking to the place page on Google Maps
