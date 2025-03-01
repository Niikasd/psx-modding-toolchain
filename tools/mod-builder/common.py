import os
import sys
import copy

remaining_args = copy.deepcopy(sys.argv[1:])

CONFIG_FILE = "config.json"

def cli_pause() -> None:
    if len(sys.argv) > 1:
        sys.exit(0) if len(remaining_args) == 0 else print("Continuing...")
    else:
        print("Press Enter to continue...")
        input()

def get_distance_to_config(print_error: bool) -> str:
    if print_error:
        print("No config.json found. Make sure to set this prerequisite file before continuing.")
        cli_pause()
    config = CONFIG_FILE
    distance = str()
    max_depth = 10
    k = 0
    failed = False
    while not os.path.isfile(config):
        distance += "../"
        config = distance + CONFIG_FILE
        k += 1
        if k == max_depth:
            failed = True
            break
    if not failed:
        return distance
    return get_distance_to_config(True)

LOG_FILE = "crash.log"
FOLDER_DISTANCE = get_distance_to_config(False)
ISO_PATH = FOLDER_DISTANCE + "build/"
SYMS_PATH = FOLDER_DISTANCE + "symbols/"
GAME_INCLUDE_PATH = FOLDER_DISTANCE + "include/"
COMPILE_LIST = "buildList.txt"
OUTPUT_FOLDER = "output/"
BACKUP_FOLDER = "backup/"
DEBUG_FOLDER = "debug/"
GCC_MAP_FILE = DEBUG_FOLDER + "mod.map"
REDUX_MAP_FILE = DEBUG_FOLDER + "redux.map"
CONFIG_PATH = FOLDER_DISTANCE + CONFIG_FILE
SETTINGS_PATH = FOLDER_DISTANCE + "../settings.json"
DISC_PATH = FOLDER_DISTANCE + "disc.json"
COMMENT_SYMBOL = "//"
MOD_NAME = os.getcwd().replace("\\", "/").split("/")[-1]
HEXDIGITS = ["A", "B", "C", "D", "E", "F"]

def check_file(filename: str) -> bool:
    if not os.path.isfile(filename):
        print("[Common-py] ERROR: no " + filename + " found.")
        return False
    return True

def check_prerequisite_files() -> bool:
    status = check_file(COMPILE_LIST)
    status = check_file(DISC_PATH) and status
    status = check_file(SETTINGS_PATH) and status
    if not status:
        print("[Common-py] Please set up these prerequisite files before continuing.")

    return status

def create_directory(dirname: str) -> None:
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

def request_user_input(first_option: int, last_option: int, error_msg: str) -> int:
    if len(sys.argv) > 1 and len(remaining_args) == 0:
        incomplete_args_msg = "ERROR: Not enough arguments to complete command."
        print(incomplete_args_msg)
        raise Exception(incomplete_args_msg)

    i = 0
    while True:
        try:
            i = int(input()) if len(sys.argv) < 2 else int(remaining_args.pop(0))
            if (i < first_option) or (i > last_option):
                print(error_msg)
                if (sys.argv > 1):
                    sys.exit(1)
            else:
                break
        except:
            print(error_msg)
            if (sys.argv > 1):
                sys.exit(1)
    return i

def get_build_id() -> int:
    if not os.path.isfile("Makefile"):
        return None
    with open("Makefile", "r") as file:
        for line in file:
            line = line.split()
            if len(line) and line[0] == "CPPFLAGS":
                build_var = line[-1]
                build_id = int(build_var.split("=")[-1].strip())
                return build_id

def is_number(s: str) -> bool:
    is_hex = False
    if len(s) > 1 and s[0] == "-":
        s = s[1:]
    if len(s) > 2 and s[:2] == "0x":
        s = s[2:]
        is_hex = True
    for char in s:
        if not ((char.isdigit()) or (is_hex and char.upper() in HEXDIGITS)):
            return False
    return True

def cli_clear() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def check_compile_list() -> bool:
    if os.path.isfile(COMPILE_LIST):
        return True
    return False