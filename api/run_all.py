import subprocess
import sys
import os
from threading import Thread

def run_api():
    os.chdir('api')
    subprocess.run([
        sys.executable, '-m', 'uvicorn', 'main:app',
        '--host', '0.0.0.0', '--port', os.getenv('PORT', '8000')
    ])

def run_bot():
    os.chdir('bot')
    subprocess.run([sys.executable, 'main.py'])

if __name__ == '__main__':
    # Run API in background
    api_thread = Thread(target=run_api, daemon=True)
    api_thread.start()

    # Run bot in main thread
    run_bot()
