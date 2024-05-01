Ziiiii
=====
A cool discord bot

The origin story
-----
This project originally started as a project for my discord server. As the said discord server is no more, I have decided to generalize this project for use in any discord server. Have fun with it!

How to use
-----
This codebase is built on the Python pycord library.  
Before doing anything, you will need to create a discord bot. You are responsible for getting information on how to do so.  
Next, you will need to create a .env file in the bot directory. It should look like this:
```
BOT_TOKEN=<the token for your bot>
HOME_GUILD_ID=<the id of home guild (server) of the bot>
ENABLED_MODULES=<comma-separated list of enabled modules>
# CraftyController stuff only required if using mc module
CRAFTYCONTROLLER_URL=<url of craftycontroller for mc module>
CRAFTYCONTROLLER_API_TOKEN=<craftycontroller api token with superuser perms>
CRAFTYCONTROLLER_ROLE_ID=<id of craftycontroller role for servers to use>
```
After setting up your .env file, you can run the bot using Docker:
```sh
docker compose up --build
```

Usage terms
-----
### By:
- Using this bot or any forks/derivatives of it in your server
- Forking this codebase
- Deriving code from this codebase

### You agree to the following terms:
#### Credit:
- Provide credit to me (Nater0214) in the following places:
  - The bot's description
  - The bot's repository/codebase
  - Anywhere else you see fit
- Provide credit to this repository in the following places:
  - The bot's description
    - This is optional if you are using this codebase and not a fork/derivative.
  - The bot's repository/codebase
  - Anywhere else you see fit
#### Licensing:
- Adhere to the GNU GPL v3.0 (Included in this repository). This means:
  - Your codebase **must** be open-source, easily accessible, and readily available to all of your bot's users and anyone else who may wish to view it. I recommend you provide a link to the codebase in the bot's description.
  - Your codebase **must** also use and include the GNU GPL v3.0 license.
#### Terms modification:
- You **must** include these terms in your codebase.
- You may extend these terms without modifying existing terms.
- When these terms are updated, you **must** reflect the changes in the terms of your codebase.
  - If an update to these terms adds a term that you have already added in your extensions, the update to these terms takes priority.
#### Liability:
- I (Nater0214) am not responsible for any misuse of this codebase or any forks/derivatives of it.
