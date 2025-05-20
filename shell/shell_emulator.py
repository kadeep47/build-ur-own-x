import os
import sys
import logging
import subprocess


def setup_logging():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def find_in_path(cmd_name):
    """
    Search for a command in PATH directories. Return the full path if found, else None.
    """
    for path_dir in os.getenv("PATH", "").split(os.pathsep):
        candidate = os.path.join(path_dir, cmd_name)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def main():
    setup_logging()
    logging.warning("Starting shell emulator")

    while True:
        try:
            # Prompt the user
            cmd_line = input("Hello $: ")
        except EOFError:
            print()  # newline
            logging.warning("EOF received, exiting")
            break
        except KeyboardInterrupt:
            print()  # newline
            logging.warning("KeyboardInterrupt, exiting")
            break

        cmd_line = cmd_line.strip()
        if not cmd_line:
            print("No command entered, try again.")
            continue

        parts = cmd_line.split()
        cmd = parts[0]
        args = parts[1:]
        logging.warning(f"Received command: {cmd} with args: {args}")

        # Builtin: exit
        if cmd == "exit":
            exit_code = 0
            if args and args[0].isdigit():
                exit_code = int(args[0])
            logging.warning(f"Exiting with code {exit_code}")
            sys.exit(exit_code)

        # Builtin: echo
        if cmd == "echo":
            message = " ".join(args)
            print(message)
            continue

        # Builtin: type
        if cmd == "type":
            if not args:
                print("Usage: type <command> [<command> ...]")
                continue
            for name in args:
                if name in ("echo", "type", "exit"):
                    print(f"{name} is a shell builtin command")
                else:
                    path_found = find_in_path(name)
                    if path_found:
                        print(f"{name} found at {path_found}")
                    else:
                        print(f"{name}: command not found in PATH")
            continue

        # External commands
        exe_path = find_in_path(cmd)
        if exe_path:
            try:
                result = subprocess.run([exe_path] + args,
                                        capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout, end="")
                if result.stderr:
                    print(result.stderr, file=sys.stderr, end="")
            except Exception as e:
                print(f"Error running command '{cmd}': {e}")
            continue

        # Command not found
        print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()
