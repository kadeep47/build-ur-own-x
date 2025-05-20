import os
import sys
import time
import logging
import subprocess
import signal
import threading
import json


def main():
    logging.warning(f"inside main")
    while True:
        # logging.warning(f"infinte true loop")
        sys.stdout.write(" Hello $:")
        sys.stdout.flush()
        cmd = input()
        logging.warning(f" current cmd {cmd}")
        if cmd  == "exit()":
            exit
        else: 
            print(f" {cmd} : command not found")


logging.warning(f"name where it's running {__name__}")
if __name__ == "__main__":
    main()