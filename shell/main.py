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

        cmd_string = cmd.split(" ")
        logging.warning(f" current base cmd {cmd_string[0]}")

        if cmd_string[0] ==  "exit":
            if cmd_string[1].isdigit and  len(cmd_string[1]) > 1: 
                sys.exit(int(cmd_string[1]))
        elif cmd_string[1] == "echo":
            sys.stdout.write("".join(cmd_string[1])  + "\n")

        
        


logging.warning(f"name where it's running {__name__}")
if __name__ == "__main__":
    main()