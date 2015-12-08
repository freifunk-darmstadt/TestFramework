import yaml
import io
import logging
import os.path
from server.router import *


class ConfigManager:

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # This is your Project Root
    CONFIG_PATH = os.path.join(BASE_DIR, 'config')  # Join Project Root with config
    ROUTER_AUTO_CONFIG_PATH = os.path.join(CONFIG_PATH, 'router_auto_config.yaml')
    ROUTER_MANUAL_CONFIG_PATH = os.path.join(CONFIG_PATH, 'router_manual_config.yaml')
    SERVER_CONFIG_PATH = os.path.join(CONFIG_PATH, 'server_config.yaml')
    TEST_CONFIG_PATH = os.path.join(CONFIG_PATH, 'test_config.yaml')

    @staticmethod
    def read_file(path: str = "") -> []:
        try:
            if path == "":
                logging.error("Path is an empty string")
                return
            file_stream = io.open(path, "r", encoding="utf-8")
            output = yaml.safe_load(file_stream)
            file_stream.close()
            return output
        except IOError as ex:
            logging.error("Error at read the file at path: {0}\nError: {1}".format(path, ex))
        except yaml.YAMLError as ex:
            logging.error("Error at safe load the YAML-File\nError: {0}".format(ex))

    @staticmethod
    def write_file(data: str = "", path: str = "") -> None:
        try:
            if path == "":
                logging.error("Path is an empty string")
                return
            file_stream = io.open(path, "w", encoding="utf-8")
            yaml.safe_dump(data, file_stream)
            file_stream.flush()
            file_stream.close()
        except IOError as ex:
            logging.error("Error at read the file at path: {0}\nError: {1}".format(path, ex))
        except yaml.YAMLError as ex:
            logging.error("Error at safe dump the YAML-File\nError: {0}".format(ex))

    @staticmethod
    def get_router_auto_config() -> []:
        return ConfigManager.read_file(ConfigManager.ROUTER_AUTO_CONFIG_PATH)

    @staticmethod
    def get_router_auto_list(count: int = 0) -> []:
        output = ConfigManager.get_router_auto_config()

        if not len(output) == 8:
            logging.error("List must be length of 8 but has a length of {0}".format(len(output)))
            return

        try:
            router_count = output[0]
            name = output[1]
            identifier = output[2]
            ip = output[3]
            mask = output[4]
            username = output[5]
            password = output[6]
            power_socket = output[7]

            i = identifier['default_Start_Id']
            socket_id = power_socket['powerSocket_Start_Id']
            router_list = []

            if count <= 0:
                count = router_count['router_Count']
            else:
                count = count

            for x in range(0, count):
                v = Router(name['default_Name'] + "{0}".format(i), i, ip['default_IP'], mask['default_Mask'],
                           username['default_Username'], password['default_Password'], socket_id)
                router_list.append(v)
                i += 1
                socket_id += 1

            return router_list

        except Exception as ex:
            logging.error("Error at building the list of Router's\nError: {0}".format(ex))

    @staticmethod
    def get_router_manual_config() -> []:
        return ConfigManager.read_file(ConfigManager.ROUTER_MANUAL_CONFIG_PATH)

    @staticmethod
    def get_router_manual_list() -> []:
        output = ConfigManager.get_router_manual_config()

        router_list = []

        for i in range(0, len(output)):
            router_info = output[i]

            if not len(router_info) == 7:
                logging.error("List must be length of 7 but has a length of {0}".format(len(output)))
                return

            try:
                v = Router(router_info['Name'], router_info['Id'], router_info['IP'], router_info['Mask'],
                           router_info['Username'], router_info['Password'], router_info['PowerSocket'])
                router_list.append(v)

            except Exception as ex:
                logging.error("Error at building the list of Router's\nError: {0}".format(ex))

        return router_list

    @staticmethod
    def get_server_config() -> []:
        return ConfigManager.read_file(ConfigManager.SERVER_CONFIG_PATH)

    @staticmethod
    def get_server_property_list() -> []:
        output = ConfigManager.get_server_config()
        return output

    @staticmethod
    def get_test_config() -> []:
        return ConfigManager.read_file(ConfigManager.TEST_CONFIG_PATH)

    @staticmethod
    def get_test_list() -> []:
        output = ConfigManager.get_test_config()
        return output