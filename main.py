# main.py
# Ziiiii Bot
# A cool discord bot


# Imports
import signal

from src import bot


# Definitions
def main() -> None:
    """Main function"""

    print("Program started")

    bot.run()


# Run
if __name__ == "__main__":
    # Add kill signals
    signal.signal(signal.SIGINT, exit)
    signal.signal(signal.SIGTERM, exit)

    main()
    exit(0)
