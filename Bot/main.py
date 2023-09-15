# main.py
# Ziiiii Bot
# Does random stuff in the Ziiiii Server


# Imports
import signal

from dotenv import load_dotenv

from src import bot


# Definitions
def main() -> None:
    """Main function"""
    
    print("Program started")
    load_dotenv()
    
    bot.run()


# Run
if __name__ == "__main__":
    # Add kill signals
    signal.signal(signal.SIGINT, exit)
    signal.signal(signal.SIGTERM, exit)
    
    main()
    exit(0)