#This is the main file used to run the decoy ssh server
#Uses Paraminko external library
#Starter code Reference: Basic SSH Honeypot by Simon Bell
#https://github.com/sjbell/basic_ssh_honeypot
#------------------------------------------------------------
#------------------------------------------------------------
#!/usr/bin/env python
import argparse
import cmd
import threading
import socket
import sys
import os
import traceback
import logging
import json
import logging
import paramiko
from datetime import datetime
from binascii import hexlify
from paramiko.util import b, u
from base64 import decodebytes

HOST_KEY = paramiko.RSAKey(filename='server.key')
SSH_BANNER = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"

UP_KEY = '\x1b[A'.encode()
DOWN_KEY = '\x1b[B'.encode()
RIGHT_KEY = '\x1b[C'.encode()
LEFT_KEY = '\x1b[D'.encode()
BACK_KEY = '\x7f'.encode()

#logger setup to log the attacks the honeypot recieves.  Send to file ssh_honeypot.log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='ssh_honeypot.log')

# Fake filesystem structure
fake_filesystem = {
    "/": ["home"],
    "/home": ["root"],
    "/home/root": ["readme.txt", "documents", "files"],
    "/home/root/documents": ["secrets.txt"],
    "/home/root/files": ["employee_info.txt"]
}

# Fake file contents
fake_file_contents = {
    "readme.txt": "This server is intended for development purposes only. Please follow all proper guidelines to ensure a stable and secure environment.",
    "secrets.txt": "Bucky's real name is John Doe!",
    "employee_info.txt": """Name: Dave Smith
Position: Senior Engineer
Email: davesmith@hoenybee.com
Phone: (555) 123-4567
Salary: $120,000"""
}

# Current directory tracker
fake_current_dir = "/home/root"

# Generates a realistic shell prompt with the current directory
def get_prompt():
    return f"{attacker_username}@dev-ssh-01:{fake_current_dir} $ "

#This Function processes commands sent by the client and responds with predefined outputs. The fake filesystem is used to trick the attacker into thinking they are navigating a real directory.
def handle_cmd(cmd, chan, ip):

    global fake_current_dir

     # Just some common fake command responses
    command_responses = {
        "pwd": fake_current_dir,
        "whoami": "root",
        "date": datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y"),
        "echo hello world": "hello world",
        "cat /etc/hostname": "admin_server"
    }

    # Handle the 'ls' command
    if cmd.strip() == "ls":
        if fake_current_dir in fake_filesystem:
            files = fake_filesystem[fake_current_dir]
            formatted_ls = " ".join(files)  # Join filenames with spaces
            chan.send(f"{formatted_ls}\r\n")
        else:
            chan.send(f"-bash: ls: cannot access '{fake_current_dir}': No such file or directory\r\n")
            return

    # Handle 'cd' command
    elif cmd.startswith("cd "):
        target_dir = cmd.split(" ", 1)[1]

        if target_dir == "../":
            if fake_current_dir != "/home/root":
                fake_current_dir = "/home/root"
        elif target_dir in fake_filesystem.get(fake_current_dir, []):
            fake_current_dir = f"{fake_current_dir}/{target_dir}" if fake_current_dir != "/" else f"/{target_dir}"
        else:
            chan.send(f"-bash: cd: {target_dir}: No such file or directory\r\n")
            return

        return

    # Handle 'cat' for fake files
    elif cmd.startswith("cat "):
        filename = cmd.split(" ", 1)[1]

        if filename in fake_filesystem.get(fake_current_dir, []):
            # Format the response correctly with \r\n
            file_content = fake_file_contents.get(filename, "").strip()
            formatted_content = "\r\n".join(file_content.split("\n"))  # Ensure clean formatting

            chan.send(f"{formatted_content}\r\n\r\n")  # Double \r\n for cleaner output
        else:
            chan.send(f"-bash: cat: {filename}: No such file or directory\r\n")
            return


    # Default response if command isn't recognized
    else:
        response = command_responses.get(cmd, None)  # Default to None if not recognized

        # Only send the default response if the command wasn't recognized
        if response is None:
            response = f"bash: {cmd}: command not found"

        if response:
            logging.info(f'Response from honeypot ({ip}): {response}')
            response = response + "\r\n"

        chan.send(response)  # Ensure prompt is printed after response


#basic honeypot implementation using python paramiko server interface
attacker_username = None
class BasicSshHoneypot(paramiko.ServerInterface):

    #stores the client IP
    client_ip = None


    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event = threading.Event()


    #This method will be called when the client requests a new channel (executes a command)
    def check_channel_request(self, kind, chanid):
        logging.info('client called check_channel_request ({}): {}'.format(
                    self.client_ip, kind))
        if kind == 'session':
            #if the channel type is sesion, the return indicates taht the server allows this type of session
            return paramiko.OPEN_SUCCEEDED

    #Returns the types of authentication methods allowed for a client
    #pub key and passwords are supported
    def get_allowed_auths(self, username):
        logging.info('client called get_allowed_auths ({}) with username {}'.format(
                    self.client_ip, username))
        return "publickey,password"

    #handles pub key authentication from the client
    def check_auth_publickey(self, username, key):
        fingerprint = u(hexlify(key.get_fingerprint()))
        logging.info('client public key ({}): username: {}, key name: {}, md5 fingerprint: {}, base64: {}, bits: {}'.format(
                    self.client_ip, username, key.get_name(), fingerprint, key.get_base64(), key.get_bits()))
        return paramiko.AUTH_PARTIALLY_SUCCESSFUL

    #handles password authentication from the client
    def check_auth_password(self, username, password):
        #capture the attackers username during authentication to be displayed later
        global attacker_username
        attacker_username = username
        # Accept all passwords as valid by default
        logging.info('new client credentials ({}): username: {}, password: {}'.format(
                    self.client_ip, username, password))


        return paramiko.AUTH_SUCCESSFUL

    #called when the client requests a shell session
    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    #called when client requests a pseudo-terminal.
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    #called when the client requests to execute a command
    def check_channel_exec_request(self, channel, command):
        command_text = str(command.decode("utf-8"))
        #decodes command and logs it
        logging.info('client sent command via check_channel_exec_request ({}): {}'.format(
                    self.client_ip, username, command))
        #always return true showing the command execution request is always allowed
        return True


def handle_connection(client, addr,):

    client_ip = addr[0]
    logging.info('New connection from: {}'.format(client_ip))
    print('New connection is here from: {}'.format(client_ip))

    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        transport.local_version = SSH_BANNER # Change banner to appear more convincing
        server = BasicSshHoneypot(client_ip)
        try:
            transport.start_server(server=server)

        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
            raise Exception("SSH negotiation failed")

        # wait for auth
        chan = transport.accept(20)
        if chan is None:
            print('*** No channel (from '+client_ip+').')
            raise Exception("No channel")

        chan.settimeout(20)

        if transport.remote_mac != '':
            logging.info('Client mac ({}): {}'.format(client_ip, transport.remote_mac))

        if transport.remote_compression != '':
            logging.info('Client compression ({}): {}'.format(client_ip, transport.remote_compression))

        if transport.remote_version != '':
            logging.info('Client SSH version ({}): {}'.format(client_ip, transport.remote_version))

        if transport.remote_cipher != '':
            logging.info('Client SSH cipher ({}): {}'.format(client_ip, transport.remote_cipher))

        server.event.wait(20)
        if not server.event.is_set():
            logging.info('** Client ({}): never asked for a shell'.format(client_ip))
            raise Exception("No shell request")

        try:
            chan.send("Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-128-generic x86_64)\r\n\r\n")
            run = True
            while run:
                chan.send(get_prompt())
                command = ""
                while not command.endswith("\r"):
                    transport = chan.recv(1024)
                    print(client_ip+"- received:",transport)
                    # Echo input to psuedo-simulate a basic terminal

                    if transport == BACK_KEY:
                        if command:
                            #remove the last character from the command
                            command = command[:-1]
                            #send backspace and space to simulate removing the character
                            chan.send(b'\b \b')
                    elif (
                            transport != UP_KEY
                            and transport != DOWN_KEY
                            and transport != LEFT_KEY
                            and transport != RIGHT_KEY
                            ):
                        chan.send(transport)
                        command += transport.decode("utf-8")

                chan.send("\r\n")
                command = command.rstrip()
                logging.info('Command receied ({}): {}'.format(client_ip, command))

                if command == "exit":
                    settings.addLogEntry("Connection closed (via exit command): " + client_ip + "\n")
                    run = False
                elif command == "":
                    # Handle just pressing Enter: send a newline to simulate terminal behavior
                     chan.send("\r\n")

                else:
                    handle_cmd(command, chan, client_ip)

        except Exception as err:
            print('!!! Exception: {}: {}'.format(err.__class__, err))
            try:
                transport.close()
            except Exception:
                pass

        chan.close()

    except Exception as err:
        print('!!! Exception: {}: {}'.format(err.__class__, err))
        try:
            transport.close()
        except Exception:
            pass


def start_server(port, bind):
    """Init and run the ssh server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind, port))
    except Exception as err:
        print('*** Bind failed: {}'.format(err))
        traceback.print_exc()
        sys.exit(1)

    threads = []
    while True:
        try:
            sock.listen(100)
            print('Listening for connection on port {} ...'.format(port))
            client, addr = sock.accept()
        except Exception as err:
            print('*** Listen/accept failed: {}'.format(err))
            traceback.print_exc()
        new_thread = threading.Thread(target=handle_connection, args=(client, addr))
        new_thread.start()
        threads.append(new_thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run an SSH honeypot server')
    parser.add_argument("--port", "-p", help="The port to bind the ssh server to (default 22)", default=2222, type=int, action="store")
    parser.add_argument("--bind", "-b", help="The address to bind the ssh server to", default="", type=str, action="store")
    args = parser.parse_args()
    start_server(args.port, args.bind)
