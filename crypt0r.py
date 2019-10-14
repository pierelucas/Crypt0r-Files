# Crypt0r - A Tool for simple file encryption and decryption
#
# Creation:    14.10.2019
# Last Update: 14.10.2019
#
#
# MIT License
#
# Copyright (c) 2019 by PiereLucas
# https://github.com/pierelucas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#
# Modules
#
import os, shutil, time, random, sys, string, subprocess
from colorama import Fore, Style
from cryptography.fernet import Fernet


class Crypt0r():
    """
    File Cryptor Class with modules
    """

    def __init__(self):

        # Time
        self.lt = time.localtime()
        self.time_hm = time.strftime(Fore.GREEN + "%H:%M" + Style.RESET_ALL, self.lt)

        # Banner
        self.banner_txt = time.strftime("""
         ______   ______    __  __   ______   _________  ______   ______       
        /_____/\ /_____/\  /_/\/_/\ /_____/\ /________/\/_____/\ /_____/\      
        \:::__\/ \:::_ \ \ \ \ \ \ \\:::_ \ \\__.::.__\/\:::_ \ \\:::_ \ \     
         \:\ \  __\:(_) ) )_\:\_\ \ \\:(_) \ \  \::\ \   \:\ \ \ \\:(_) ) )_   
          \:\ \/_/\\: __ `\ \\::::_\/ \: ___\/   \::\ \   \:\ \ \ \\: __ `\ \  
           \:\_\ \ \\ \ `\ \ \ \::\ \  \ \ \      \::\ \   \:\_\ \ \\ \ `\ \ \ 
            \_____\/ \_\/ \_\/  \__\/   \_\/       \__\/    \_____\/ \_\/ \_\/ 

                    Coded by PiereLucas    |   github.com/pierelucas   
                                         %H:%M 
                                         [-V-]                                                     
        """, self.lt)

        self.menu_txt = """
[1] Encrypt     [99] Generate Key // Crypt0r will Backup your old Key!
[2] Decrypt     [Else] Exit
        """

        # Details
        self.version = "V: 1.0"

        # Crypt0r
        self.key = None

    def inp(self):

        while True:
            print(self.menu_txt)
            choice = str(input(self.time_hm + Fore.GREEN + " [+] Which option Number » "))
            print(Style.RESET_ALL)
            if choice == '1':
                return self.file_inp(), 'encrypt'
            elif choice == '2':
                return self.file_inp(), 'decrypt'
            elif choice == '99':
                if self.gen_key():
                    print("[+] Key Generated")
                    _true, backup_need, backup_path = self.write_key()
                    if _true:
                        print("[+] Key saved to file")
                        print()
                        if backup_need:
                            print(self.time_hm + Fore.GREEN + " [+] Backup key saved as " + Fore.CYAN + backup_path + Fore.GREEN + " in " + Fore.CYAN + self.path_name(backup_path) + Style.RESET_ALL)
                            continue
            else:
                print("All Systems Down")
                sys.exit(0)

    def file_inp(self):

        while True:
            file_path = str(input(self.time_hm + Fore.GREEN + " [+] File Path » "))
            print(Style.RESET_ALL)
            if os.path.isfile(file_path):
                return file_path
            else:
                continue

    def is_file(self):

        try:
            if os.path.isfile("key.crypt0r"):
                return True
            else:
                return False
        except PermissionError:
            print("No Permission")
            print("All Systems Down")
            sys.exit(0)

    def path_name(self, path):

        pn = os.path.dirname(path)
        if pn != "": return pn
        else: return "Aktive Directory"

    def rand_str(self, stringlen=6):

        letters = string.ascii_lowercase + string.digits
        return "".join(random.choice(letters) for i in range(stringlen))

    def gen_key(self):

        try:
            self.key = Fernet.generate_key()
            self.crypt = Fernet(self.key)
            return True

        except PermissionError:
            print("No Permission")
            print("All Systems Down")
            sys.exit(0)

    def write_key(self):

        backup_need = False
        backup_path = None
        if os.path.isfile("key.crypt0r"):
            backup_path = self.backup_key()
            backup_need = True
        with open("key.crypt0r", 'wb') as f:
            f.write(self.key)
            return True, backup_need, backup_path

    def read_key(self):

        with open("key.crypt0r", 'rb') as f:
            self.key = f.read()
            self.crypt = Fernet(self.key)
            return True

    def backup_key(self):

        backup_path = "key_old_" + self.rand_str() + ".crypt0r"
        shutil.move("key.crypt0r", backup_path)
        return backup_path

    def enc(self, *, file_path):

        with open(file_path, 'rb') as f:
            file_data = f.read()
            encrypted_data = self.crypt.encrypt(file_data)

        with open(file_path, 'wb') as f:
            f.write(encrypted_data)

        return True

    def dec(self, *, file_path):

        with open(file_path, 'rb') as f:
            file_data = f.read()

        decrypted_data = self.crypt.decrypt(file_data)

        with open(file_path, 'wb') as f:
            f.write(decrypted_data)

        return True

    def run(self):

        subprocess.call("clear", shell=True)
        print(Fore.CYAN + self.banner_txt.replace("[-V-]", self.version) + Style.RESET_ALL)

        if self.is_file():
            if self.read_key():
                print("[+] Key loaded")
        else:
            if self.gen_key():
                print("[+] Key Generated")
                if self.write_key():
                    print("[+] Key saved to file")

        file_path, _mode = self.inp()

        if _mode == 'encrypt':
            if self.enc(file_path=file_path):
                print("[+] Success encrypt file " + file_path + " in " + self.path_name(file_path))
                sys.exit(0)
        elif _mode == 'decrypt':
            if self.dec(file_path=file_path):
                print("[+] Success decrypt file " + file_path + " in " + self.path_name(file_path))
                sys.exit(0)


# TO BE CONTINUED ...
cryptor = Crypt0r()
cryptor.run()
