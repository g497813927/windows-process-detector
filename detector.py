# -*- coding: utf-8 -*-
"""
Author:     Jiacheng Zhao
Email:      admin@techzjc.com
Version:    0.1
Date:       2021-11-25
Description:
    This file utilizes the wmi module to provide several functions to detect the current process.
"""


class Detector(object):

    def __init__(self, ip='localhost', user=None, password=None):
        """
            Initialize the detector object.
            :param ip: the ip address of the target machine
            :param user: the username of the target machine
            :param password: the password of the target machine
        """
        # check whether pip package is installed
        # noinspection PyBroadException
        try:
            import pip
        except Exception:
            print("Please install pip first.")
            exit()

        # detect whether a package is installed, if not, install it directly
        try:
            import wmi
        except ImportError:
            pip.main(['install', 'wmi'])
            import wmi

        if ip == 'localhost' or ip == '127.0.0.1' or ip is None or ip == '':
            # case when detecting the local machine
            self.wmi_obj = wmi.WMI()
        else:
            # case when detecting the remote machine
            if user is None or password is None:
                raise ValueError('The user and password cannot be None when detecting the remote machine.\n'
                                 'Please input user and password as arguments into the constructor!')
            self.wmi_obj = wmi.WMI(computer=ip, user=user, password=password)

    def detect_process_based_on_path(self, process_path):
        """
            Detect whether a process exists based on the given process executable path.
            :param process_path: the path of the process executable
            :raise ValueError: if the process_path is None or not a string
            :return: The process object list
        """
        # Check if the process_path is a string or is None
        if not isinstance(process_path, str) or process_path is None or process_path == '':
            raise TypeError('The process_path should be a string!')
        # Get the process object list
        wql = "SELECT * FROM Win32_Process WHERE ExecutablePath = '{}'".format(process_path)
        return self.wmi_obj.query(wql)

    def detect_process_based_on_name(self, process_name):
        """
            Detect whether a process exists based on the given process name.
            :param process_name: the name of the process
            :raise ValueError: if the process_name is None or not a string
            :return: The process object list
        """
        # Check if the process_name is a string or is None
        if not isinstance(process_name, str) or process_name is None or process_name == '':
            raise TypeError('The process_name should be a string!')
        # Get the process object list
        wql = "SELECT * FROM Win32_Process WHERE Name = '{}'".format(process_name)
        return self.wmi_obj.query(wql)

    def detect_thread_based_on_process_handle_id(self, process_handle_id):
        """
            Detect whether a thread exists based on the given process handle id.
            :param process_handle_id: the process handle id
            :raise ValueError: if the process_handle_id is None or not an integer
            :return: The thread object list
        """
        # Check if the process_handle_id is an integer or is None
        if not isinstance(process_handle_id, int) or process_handle_id is None or process_handle_id == '':
            raise TypeError('The process_handle_id should be an integer!')
        # Get the thread object list
        wql = "SELECT * FROM Win32_Thread WHERE ProcessId = {}".format(process_handle_id)
        return self.wmi_obj.query(wql)

    def detect_thread_based_on_thread_id(self, thread_id):
        """
            Detect whether a thread exists based on the given thread id.
            :param thread_id: the thread id
            :raise ValueError: if the thread_id is None or not an integer
            :return: The thread object list
        """
        # Check if the thread_id is an integer or is None
        if not isinstance(thread_id, int) or thread_id is None or thread_id == '':
            raise TypeError('The thread_id should be an integer!')
        # Get the thread object list
        wql = "SELECT * FROM Win32_Thread WHERE ThreadId = {}".format(thread_id)
        return self.wmi_obj.query(wql)

    def launch_program_based_on_path(self, program_path, arguments=None):
        """
            Launch a program based on the given program path.
            :param program_path: the path of the program executable
            :param arguments: the arguments of the program
            :raise ValueError: if the program_path is None or not a string
            :return: The process object
        """
        # Check if the program_path is a string or is None
        if not isinstance(program_path, str) or program_path is None or program_path == '':
            raise TypeError('The program_path should be a string!')
        # Launch the program
        return self.wmi_obj.Win32_Process.Create(CommandLine='{} {}'.format(program_path, arguments))

    def restart_program_based_on_path(self, program_path, arguments=None):
        """
            Restart a program based on the given program path.
            :param program_path: the path of the program executable
            :param arguments: the arguments of the program
            :raise ValueError: if the program_path is None or not a string
            :return: The process object
        """
        # Check if the program_path is a string or is None
        if not isinstance(program_path, str) or program_path is None or program_path == '':
            raise TypeError('The program_path should be a string!')
        # Get the process object list
        process_obj_list = self.detect_process_based_on_path(program_path)
        # Check if the process object list is empty
        if not len(process_obj_list) == 0:
            # Kill the process
            for process_obj in process_obj_list:
                process_obj.Terminate()
        # Launch the program
        return self.wmi_obj.Win32_Process.Create(CommandLine='{} {}'.format(program_path, arguments))

    def kill_program_based_on_path(self, program_path):
        """
            Kill a program based on the given program path.
            :param program_path: the path of the program executable
            :raise ValueError: if the program_path is None or not a string
            :return: True if the program is killed successfully, False otherwise
        """
        # Check if the program_path is a string or is None
        if not isinstance(program_path, str) or program_path is None or program_path == '':
            raise TypeError('The program_path should be a string!')
        # Get the process object list
        process_obj_list = self.detect_process_based_on_path(program_path)
        # Check if the process object list is empty
        if not len(process_obj_list) == 0:
            # Kill the process
            # noinspection PyBroadException
            try:
                for process_obj in process_obj_list:
                    process_obj.Terminate()
            except Exception:
                return False
        return True

    def launch_program_based_on_name(self, program_name, arguments=None):
        """
            Launch a program based on the given program name.
            :param program_name: the name of the program
            :param arguments: the arguments of the program
            :raise ValueError: if the program_name is None or not a string
            :return: The process object
        """
        # Check if the program_name is a string or is None
        if not isinstance(program_name, str) or program_name is None or program_name == '':
            raise TypeError('The program_name should be a string!')
        # Get the program path
        program_path = self.detect_process_based_on_name(program_name)
        # Launch the program
        return self.wmi_obj.Win32_Process.Create(CommandLine='{} {}'.format(program_path, arguments))

    def detect_thread_list_based_on_process_obj(self, process_obj):
        """
            Detect the thread list of the given process object.
            :param process_obj: the process object
            :raise ValueError: if the process_obj is None
            :return: The thread list
        """
        # Check if the process_obj is None
        if process_obj is None:
            raise TypeError('The process_obj should not be None!')
        # Get the thread list
        wql = 'SELECT * FROM Win32_Thread WHERE ProcessHandle = {}'.format(process_obj.Handle)
        return self.wmi_obj.query(wql)

    @staticmethod
    def detect_thread_list_contain_other_than_status_code(thread_list, status_code):
        """
            Detect whether a thread list contains a specific status code.
            :param thread_list: the thread object list
            :param status_code: the status code
            :raise ValueError: if the thread_list is None or not a list
            :return: True if the thread_list contains the status code, False otherwise
        """
        # Check if the thread_list is a list or is None
        if not isinstance(thread_list, list) or thread_list is None or thread_list == '':
            raise TypeError('The thread_list should be a list!')
        # Check if the thread_list contains the status code
        for thread in thread_list:
            if not thread.ThreadWaitReason == status_code:
                return False
        return True

    def detect_thread_list_based_on_process_obj_and_status_code(self, process_obj, status_code):
        """
            Detect the thread list of the given process object and status code.
            :param process_obj: the process object
            :param status_code: the status code
            :raise ValueError: if the process_obj is None or the status_code is None
            :return: The thread list
        """
        # Check if the process_obj is None
        if process_obj is None:
            raise TypeError('The process_obj should not be None!')
        # Check if the status_code is None
        if status_code is None:
            raise TypeError('The status_code should not be None!')
        # Get the thread list
        wql = 'SELECT * FROM Win32_Thread WHERE ProcessHandle = {} AND ThreadWaitReason = {}'.format(process_obj.Handle, status_code)
        return self.wmi_obj.query(wql)
