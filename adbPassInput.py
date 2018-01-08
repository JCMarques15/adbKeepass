import os, getpass, sys, argparse

def main():
    # Creating instruction page
    parser = argparse.ArgumentParser(usage="python3 %(prog)s [options]")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    # If script called with arguments exists with error message
    if len(sys.argv) != 1:
        parser.error("Script called with arguments")
        print("{}".format(args))

    # Else it continues processing
    else:
        # Ask for Password
        adbInput = getpass.getpass("ADB Input: ")

        if '\t' in adbInput:
            # If it finds a tab sequence in the string it separats it on the tab sequence
            adbInput = adbInput.split('\t')
            print("Username: {}".format(adbInput[0]))
            print("Password: ********")

            # It then sends the username through the escaper function and sends a tab event after returning 
            escaper(adbInput[0])
            inputer("keyevent", "61")

            # Finally it sends the password through the escaper function and ends up with sending the "enter" key event
            escaper(adbInput[1])
            inputer("keyevent", "66")

        else:
            # Escapes the password only and sends the enter key event
            escaper(adbInput)
            inputer("keyevent", "66")

def escaper(escaping):
    # For each special character replace with an escaped sequence
    for ch in ['\\', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', ',', '<', '.', '>', '|', '[', '{', ']', '}', ';', ':', "'", '"', '/', '?']:
        if ch == '\\':
            # '\' requires two '\' to escape for adb
            escaping = escaping.replace("\\", "\\\\\\")
        elif ch == '`':
            # '`' requires three '\' to escape for adb
            escaping = escaping.replace("`", "\\\\\\`")
        elif ch == '$':
            # '$' requires three '\' to escape for adb
            escaping = escaping.replace("$", "\\\\\\$")
        elif ch == '"':
            # '"' requires escaping and clisong of in "'" for adb to process it as part of the string to send...
            escaping = escaping.replace('"', '''"'\\"'"''')
        else:
            # Everything else gets escaped with a single '\'
            escaping = escaping.replace(ch, "\\{}".format(ch))
        
    # Calls inputer with the text event and the string to be inputed
    inputer("text", escaping)

def inputer(eventType, adbEscapedInput):
    # executes the adb input command type with the escaped string
    os.system('adb shell input {} "{}"'.format(eventType, adbEscapedInput))

if __name__== "__main__":
    # Tries to call main
    try:
        main()
    
    # Handles keyboard interuption exceptions
    except KeyboardInterrupt:
        print ('\rExecution interrupted...Exiting!')
        try:
            sys.exit(0)
        except SystemExit as Err:
            print("Error exiting: {}".format(Err))