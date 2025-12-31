# DDSC Bot

Discord bot for **Deakin Data Science Club**

## Structure

```markdown
bot.py
config.py
main.py
requirements.txt
assets/
cogs/
├── events.py
├── info.py
└── signup.py
```

## Setup

### Prerequisites

- Python 3.11+
- Discord Bot Token

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd bot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory:

   ```env
   DISCORD_TOKEN=your_discord_bot_token
   ```

4. Run the bot:

   ```bash
   python main.py
   ```

## Dependencies

- `discord.py` - Discord API wrapper
- `python-dotenv` - Environment variable management
- `aiohttp` - Async HTTP client

## Deployment
