# Checkers AI Game

This is Checkers game with an optional AI opponent. The game goes through multiple phases, starting 
with core game logic and culminating in a graphical user interface (GUI).

## Running checkers
Running the GUI (Tkinter) on macOS

If you're using macOS and installed Python via Homebrew, you must use Python 3.11 to ensure Tkinter works correctly.
# One-time setup (if not already done):
brew install python-tk@3.11

# Run the game GUI with correct Python version:
- /opt/homebrew/bin/python3.11 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- python main.py (for terminal gameplay)

# Please select interpreter 3.11 for UI
press CTRL+P, type or select python
then select 3.11 venv
run command: python ui.py
# You can also create an alias for convenience:
echo 'alias py311="/opt/homebrew/bin/python3.11"' >> ~/.zshrc
source ~/.zshrc

# Now you can run:
py311 -m venv venv
