import json
from detector import Detector
import msg_handler

"""
Author:     Jiacheng Zhao
Email:      admin@techzjc.com
Version:    0.1.1
Update Date:       2022-06-27
Description:
    This file is the runner for this project.
"""

# Try reading the config path json file, if it fails, ask for the path
input_mode = False
paths = []
try:
    with open('check_path.json') as config_file:
        config = json.load(config_file)
        for item in config:
            paths.append(item['path'])
except FileNotFoundError:
    input_mode = True
except json.decoder.JSONDecodeError:
    input_mode = True

# Check if the input mode is enabled
if input_mode:
    config = []
    # Ask for the path, and add it to the paths list
    while True:
        path = input('Enter the path to the file: ')
        if path == '':
            break
        else:
            paths.append(path)

# Create a detector object
detector = Detector()

# Iterate through the paths list, and check if the path is in the process list
for path in paths:
    list_of_fit_processes = detector.detect_process_based_on_path(path)
    if not len(list_of_fit_processes) > 0:
        print('No process found for path: ' + path)
        print('Trying to start the process...')
        detector.launch_program_based_on_path(path)
    else:
        print('Process found for path: ' + path)
        print('Checking if the process is being suspended...')
        for process in list_of_fit_processes:
            thread_list = detector.detect_thread_list_based_on_process_obj(process)
            if Detector.detect_thread_list_contain_other_than_status_code(thread_list, 5):
                print('Process is suspended, trying to resume it...')
                msg_handler.handle_message('Alert', 'The process {} is being suspended! '
                                                    'DO NOT SUSPEND THIS PROCESS!'
                                           .format(process.name()))
                detector.restart_program_based_on_path(path)
