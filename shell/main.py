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
            if  len(cmd_string) > 1 and cmd_string[1].isdigit: 
                sys.exit(int(cmd_string[1]))
            else:
                sys.exit(int(0))
        
        if cmd_string[0] == "echo":
            sys.stdout.write("".join(cmd_string[1])  + "\n")
            continue
        
        if cmd_string[0] == "type":
            if (len(cmd_string ) > 1):
                for args in cmd_string[1:]:
                    if args == "echo":
                        print(f"{args} is a sheel builtin cmd \n")
                    elif args == "type":
                        print(f"{args} is a sheel builtin cmd \n")
                    else :
                        cmd_found = False
                        for path in os.getenv("PATH").split(":"):
                            if os.path.isdir(path): 
                                for file_name in os.listdir(path):
                                    if file_name == cmd_string[1]:
                                        print(f" {cmd_string[1]} found at  {path}")
                                        cmd_found = True
                                        break
                            if cmd_found:
                                break
                        if not cmd_found:
                            print(f"{args} : can be found at location need to implement this  \n")
        else:
            cmd_found = False
            for path in os.getenv("PATH").split(os.pathsep):
                if os.path.isdir(path):
                    for file_name in os.listdir(path):
                        if file_name == cmd_string[0] ;
                            result =  subprocess.run(cmd_string, capture_output = True, text = True)
                            print(result.stdout,end = "")
                            cmd_found = True
                            break
                if cmd_found : 
                    break

            if not cmd_found :               
                print( " {cmd_string} cmd not found")




logging.warning(f"name where it's running {__name__}")
if __name__ == "__main__":
    main()