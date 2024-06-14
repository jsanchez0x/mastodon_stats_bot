# -*- coding: utf-8 -*-

import sys
import inc
import requests
import traceback
from datetime import datetime

def check_internet(attempt=0):
    """Check if is connected to internet.

    Parameters:
        attempt(int): The attempt at the connectivity test.

    Return:
        bool: Connectivity status"""

    url = "http://neverssl.com/"
    max_attempts = 5
    timeout_seconds = 5

    try:
        requests.get(url, timeout=timeout_seconds)
        if inc.cfg.debug:
            print("Internet connection is available.")

        return True

    except (requests.ConnectionError, requests.Timeout) as exception:
        if attempt == max_attempts:
            return False
        else:
            attempt += 1
            if inc.cfg.debug:
                print("Internet connection is not available, attempt %d." % attempt)
                print("    Error: %s" % str(exception))

        return check_internet(attempt)

def download_file(url, filename):
    request = requests.get(url)
    if request.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in request:
                file.write(chunk)

        return True
    else:
        return False

def datetime_now(in_string=False):
    now = datetime.now()
    if in_string:
        return now.strftime("%d/%m/%Y %H:%M:%S")
    else:
        return now

def print_error(message):
    print ("%s ERROR: %s" % (datetime_now(True), message))

def custom_error(type, value, tb):
    if inc.cfg.debug:
        print("------------------------------- EXCEPTION -------------------------------")
        print("  Date:", datetime_now(True))
        print("  Type:", type)
        print("  Value:", value)
        print("  Traceback:")
        for file in traceback.format_tb(tb):
            for line in file.splitlines():
                print("   ", line)
        print("----------------------------- END EXCEPTION -----------------------------\n")
    else:
        print_error("%s > %s" % (type.__name__, value))

sys.excepthook = custom_error