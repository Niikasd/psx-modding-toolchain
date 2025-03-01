from syms import Syms
from compile_list import CompileList, free_sections
from common import COMPILE_LIST, SETTINGS_PATH, OUTPUT_FOLDER, BACKUP_FOLDER, get_build_id, request_user_input, check_compile_list

import os
import json

class Nops:
    def __init__(self) -> None:
        pass

    def load_config(self) -> None:
        with open(SETTINGS_PATH) as file:
            data = json.load(file)["nops"]
            self.comport = " " + data["comport"].upper()
            mode = data["mode"]
            self.prefix = "nops /" + mode.lower() + " "

    def fire_command(self, command: str) -> None:
        os.system(self.prefix + command + self.comport)

    def inject(self, backup: bool, restore: bool) -> None:
        sym = Syms(get_build_id())
        with open(COMPILE_LIST, "r") as file:
            for line in file:
                cl = CompileList(line, sym)
                if not cl.should_build():
                    continue
                bin = str()
                if cl.is_bin:
                    bin = cl.source[0]
                else:
                    bin = OUTPUT_FOLDER + cl.section_name + ".bin"
                backup_bin = BACKUP_FOLDER + "nops_" + cl.section_name + ".bin"
                if backup:
                    if not os.path.isfile(bin):
                        print("\n[NoPS-py] ERROR: " + bin + " not found.\n")
                        continue
                    size = os.path.getsize(bin)
                    self.fire_command("/dump " + hex(cl.address) + " " + hex(size) + " " + backup_bin)
                if restore:
                    bin = backup_bin
                if not os.path.isfile(bin):
                    print("\n[NoPS-py] ERROR: " + bin + " not found.\n")
                    continue
                self.fire_command("/bin " + hex(cl.address) + " " + bin)

    def hot_reload(self) -> None:
        if not check_compile_list():
            print("\n[NoPS-py] ERROR: " + COMPILE_LIST + " not found.\n")
            return
        print("Would you like to backup the state?")
        print("1 - Yes")
        print("2 - No")
        print("Note: this option is required if you want to uninstall the mod.")
        print("By selecting yes you'll overwrite the current backup.")
        error_msg = "ERROR: Invalid input. Please enter 1 for Yes or 2 for No."
        backup = request_user_input(first_option=1, last_option=2, error_msg=error_msg) == 1
        self.fire_command("/halt")
        self.inject(backup, False)
        self.fire_command("/cont")
        free_sections()

    def restore(self) -> None:
        if not check_compile_list():
            print("\n[NoPS-py] ERROR: " + COMPILE_LIST + " not found.\n")
            return
        self.fire_command("/halt")
        self.inject(False, True)
        self.fire_command("/cont")
        free_sections()