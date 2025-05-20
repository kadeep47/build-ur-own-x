Python Shell Emulator

A minimal Python-based shell emulator that implements a basic REPL (Read–Eval–Print Loop) with support for built‑in commands, external program execution, and standard Unix-like behaviors.

🧩 Inspiration & Resources

Build Your Own X: https://github.com/codecrafters-io/build-your-own-x
YouTube Demo: https://www.youtube.com/watch?v=55cohFUPZGY

🚀 Project Overview

This application behaves like a simple Unix shell, but written entirely in Python. It supports:

REPL Loop (read → evaluate → print → loop)

Built‑in commands: exit, echo, type

External executables via searching $PATH

Standard streams:

stdin: reading user input

stdout: normal command output

stderr: error messages

Exit status tracking ($?)

Line buffering with sys.stdout.flush() to ensure prompt visibility

⚙️ Getting Started

Clone the repo

git clone https://github.com/kadeep47/build-ur-own-x.git
cd python-shell-emulator

Run the shell

python shell_emulator.py

Interact at the Hello $: prompt:

Type commands like echo Hello World

Run system executables: ls, pwd, etc.

Use exit to quit (optionally exit 2 for code 2).

📐 Architecture & Key Concepts

1. REPL Loop

while True:
    line = input("Hello $: ")  # **read**
    # parse → evaluate → print → loop

2. Parsing & Execution

split(): splits the input into command and arguments.

Built‑ins: recognized before looking at $PATH.

External commands:

Search each directory in os.getenv('PATH')

Check for an executable file matching the command name

Invoke with subprocess.run

3. Standard Streams

stdin: input() reads from terminal

stdout: print() and subprocess.run(capture_output=True).stdout

stderr: captured stderr printed via sys.stderr

4. Flushing Output

sys.stdout.flush()

Ensures that the prompt and any buffered text are sent to the terminal immediately, rather than waiting for the buffer to fill.

5. Exit Status ($?)

Stored as the integer return code of the last command

Common values:

0 → success

1 → general error

2 → misuse of shell built‑ins

127 → command not found

Can be printed: e.g., echo $? will display the last exit code.

6. PATH Lookup & echo $PATH

$PATH: an environment variable listing directories separated by :

echo $PATH shows these directories

Our shell splits $PATH, iterates each directory, and checks for executables.

7. Error Handling

If a command is not found in $PATH, prints:

<cmd>: command not found

Exceptions during execution are caught and reported:

Error running command '<cmd>': <exception message>

🔧 Implementation Notes

Logging: Uses logging.warning() for internal state tracing.

Threading & Signals: (Reserved for future extension)

Configuration: You can adjust logging level in setup_logging().

🎯 Next Steps

Add support for input/output redirection (>, <, |)

Implement additional built‑ins: cd, export, etc.

Handle quoting/escaping in split() to support filenames with spaces.

Enjoy hacking your own Python shell!

