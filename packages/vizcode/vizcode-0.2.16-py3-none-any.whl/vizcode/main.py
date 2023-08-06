from vizcode.graph import Graph
from vizcode.command_line import Command_Line
from vizcode.constants import *
import multiprocessing
import vizcode.indexer as indexer
import os
import glob
import time
import hashlib
import pathlib

CURRENT_DIR_PATH = str(pathlib.Path(__file__).parent.absolute()) + "/"

class Parsed_File:
    def __init__(self, file_path, client):
        self.client = client
        self.file_path = file_path

# Get python files from given folder path. 
def get_files(folder_path, env_path, test_path):
    files = glob.glob(folder_path + '/**/*.py', recursive=True)

    if env_path:
        env_files = set(glob.glob(env_path + "/**/*.py", recursive=True))
        files  = [file for file in files if file not in env_files]
    else:
        files = [file for file in files if 'env/' not in file]

    if test_path:
        test_files = set(glob.glob(test_path + '/**/*.py', recursive=True))
        files  = [file for file in files if file not in test_files]

    return files

# Saves code to a file in the frontend directory. 
def save_code_to_file(file_path, code):
    hashed_name = hashlib.sha256(file_path.encode('utf-8')).hexdigest()[:16]
    new_file_path = CURRENT_DIR_PATH + PUBLIC_PATH + FILE_CODE_PATH + hashed_name + ".txt"
    with open(new_file_path, 'w+') as output_file:
        output_file.write(code)

    return

# Returns a parsed file.
def parse_file(args):
    file_path, env_path, folder_path = args

    print ("Parsing file " + file_path)

    with open(file_path, 'r') as f:
        code = f.read()

    save_code_to_file(file_path, code)
    client = indexer.start_indexer(file_path, code, env_path, [folder_path])

    return Parsed_File(file_path, client)

# Removes old code files from previous graph. 
def remove_old_code():
    files = glob.glob(CURRENT_DIR_PATH + PUBLIC_PATH + FILE_CODE_PATH + '/**/*.txt', recursive=True)
    for file in files:
        os.remove(file)
    
    return 

def main(parsed_files):

    graph = Graph("Newspark Python Example")

    graph.populate_graph(parsed_files)
    print("Built the graph.")

    graph.save_graph()
    print("Saved the graph.")
    
    print("Starting frontend application...\n")
    graph.start_frontend()

    return None

def start():

    args = Command_Line()

    # Parse the arguments from the Command Line
    folder_path = args.get_path()
    env_path = args.get_env()
    test_path = args.get_test()

    # Checks to make sure the paths for the source code, environment, test path are valid
    exists = True
    if not os.path.exists(folder_path):
        print ("Folder path does not exist.")
        exists = False
    
    if exists:
        if env_path and not os.path.exists(env_path):
            print ("Not a valid environment path, well default to global environment")
            env_path = None
        
        if test_path and not os.path.exists(test_path):
            print ("Not a valid test path, well default to None")
            test_path = None

        remove_old_code()

        files = get_files(folder_path, env_path, test_path)

        pool = multiprocessing.Pool(4)
        parsed_files = pool.map(parse_file, [(file_path, env_path, folder_path) for file_path in files])
        main(parsed_files)