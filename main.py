#!/usr/bin/env python3
import sys
import threading
from scheduler import SubscriptionScheduler
from app import run_flask


def main():
    scheduler = SubscriptionScheduler()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--once':
            scheduler.run_once()
        elif sys.argv[1] == '--web':
            print("Starting web server on http://localhost:8000")
            run_flask()
    else:
        flask_thread = threading.Thread(target=run_flask)
        flask_thread.daemon = True
        flask_thread.start()
        print("Web server running on http://localhost:8000")
        scheduler.start_scheduled()


if __name__ == '__main__':
    main()
