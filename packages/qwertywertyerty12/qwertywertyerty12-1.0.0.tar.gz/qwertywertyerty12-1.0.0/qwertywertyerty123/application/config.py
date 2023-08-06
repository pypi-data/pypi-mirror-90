import os

SERVER_ROOT = os.path.dirname(os.path.abspath(os.path.join(__file__, '../')))


class Config(object):
    log_folder = os.path.join(SERVER_ROOT, 'output/log')
    log_file_path = os.path.join(log_folder, 'log.log')
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)


    def __init__(self):
        self.__output_folder = os.path.join(SERVER_ROOT, 'output/')

    def get_output_folder(self):
        return self.__output_folder

