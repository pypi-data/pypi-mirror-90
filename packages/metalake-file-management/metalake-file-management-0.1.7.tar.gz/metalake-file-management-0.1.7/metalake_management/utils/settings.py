import json

from metalake_management.utils import messages


class GenericSettings:
    """
    Some generic utilities, e.g. reading the config.json
    """
    code_version = "0.1.0"

    def __init__(self, configuration_file="resources/connection_config.json"):
        # config.json settings
        self.main_config_file = configuration_file
        self.meta_version = None
        self.output_directory = None
        self.log_config = None
        self.suppress_azure_call = False
        self.azure_http_proxy = None
        self.azure_https_proxy = None
        self.storage_account_name = None
        self.storage_account_key = None
        self.storage_container = None
        self.azure_secrets = None
        self.file_locations = None
        self.incoming = None
        self.todo = None
        self.busy = None
        self.done = None
        self.redo = None
        self.hist = None
        self.process_locations = False
        self.download_location = "jsons"

    def get_config(self):
        """
            get the main configuration settings. default file is resources/config.json
        """
        module = __name__ + ".get_config"
        result = messages.message["undetermined"]

        try:
            with open(self.main_config_file) as config:
                data = json.load(config)
                # self.schema_directory = self.base_schema_folder + self.meta_version + "/"
                if "azure_secrets" in data:
                    self.azure_secrets = data["azure_secrets"]
                if "file_locations" in data:
                    self.file_locations = data["file_locations"]
                if "suppress_azure_call" in data:
                    if data["suppress_azure_call"] == "True":
                        self.suppress_azure_call = True
                    elif data["suppress_azure_call"] == "False":
                        self.suppress_azure_call = False
                    else:
                        print("Incorrect config value >" + data["suppress_azure_call"]
                              + "< for suppress_azure_call. Must be True or False. Will default to False")
                        self.suppress_azure_call = False
                if "download_location" in data:
                    self.download_location = data["download_location"]

            result = messages.message["ok"]

        except FileNotFoundError:
            print("FATAL:", module, "could find not main configuration file >" + self.main_config_file + "<.")
            return messages.message["main_config_not_found"]

        if self.azure_secrets is None:
            print("azure secrets are unknown. Please set azure_secrets in the main config file.")
        else:
            azure_secrets_result = self.get_azure_secrets(self.azure_secrets)
            if azure_secrets_result["code"] != "OK":
                # print("get_azure_secrets returned: " + azure_secrets_result["code"], module)
                return azure_secrets_result

        if self.file_locations is None:
            print("file locations are unknown. Please set file_locations in the main config file.")
        else:
            file_locations_result = self.get_file_locations(self.file_locations)
            if file_locations_result["code"] != "OK":
                # print("get_file_locations returned: " + file_locations_result["code"], module)
                return file_locations_result

        return result

    def get_azure_proxy(self):

        if self.azure_http_proxy == "None":
            self.azure_http_proxy = None
        if self.azure_https_proxy == "None":
            self.azure_https_proxy = None

        proxies = {
            "http": self.azure_http_proxy,
            "https": self.azure_https_proxy
        }
        return proxies

    def get_file_locations(self, config_file):
        if config_file is None:
            return messages.message["not_provided"]
        try:
            with open(config_file) as locations:
                data = json.load(locations)
                self.incoming = data["incoming"]
                self.todo = data["todo"]
                self.busy = data["busy"]
                self.done = data["done"]
                self.redo = data["redo"]
                self.hist = data["hist"]
                self.process_locations = True
        except FileNotFoundError as e:
            print("File with file_locations >" + self.file_locations + "< could not be found.")
            return messages.message["file_locations_not_found"]

        return messages.message["ok"]

    def get_azure_secrets(self, azure_secrets="resources/azure.secrets"):
        module = __name__ + ".get_azure_secrets"

        try:
            with open(azure_secrets) as azure:
                data = json.load(azure)
                result = self.determine_azure_secrets(data)

                if result["code"] != "OK":
                    print("ERROR: Determine azure secrets returned: " + result["code"])
                    return result
        except FileNotFoundError:
            print("ERROR: Cannot find provided azure_secrets file >" + self.azure_secrets + "<."
                  , module)
            return messages.message["azure_secrets_not_found"]

        return messages.message["ok"]

    def determine_azure_secrets(self, data):
        module = __name__ + ".determine_azure_secrets"

        if "meta_version" in data:
            main_meta_version = data["meta_version"][:3]
            if main_meta_version != "0.1":
                print("Unsupported meta_version >" + data["meta_version"] + "<."
                      , module)
                return messages.message["unsupported_meta_version_azure_secrets"]
        else:
            print("Backward compatible azure secrets file detected. Please update to a later version."
                  , module)

        self.storage_account_name = data["storage_account_name"]
        self.storage_account_key = data["storage_account_key"]
        self.storage_container = data["container"]
        # print("container: ", self.storage_container)
        if "azure_http_proxy" in data:
            self.azure_http_proxy = data["azure_http_proxy"]
        #    print("HTTP Proxy for Azure taken from azure secrets file: "
        #          + self.azure_http_proxy, module)
        # else:
        #    print("No HTTP Proxy for Azure found in azure secrets file. "
        #          + "This is OK if no proxy is needed or has been set through the environment variable HTTP_PROXY"
        #          , module)
        if "azure_https_proxy" in data:
            self.azure_https_proxy = data["azure_https_proxy"]
        #    print("HTTPS Proxy for Azure taken from azure secrets file: "
        #          + self.azure_https_proxy, module)
        # else:
        #    print("No HTTPS Proxy for Azure found in azure secrets file. "
        #          + "This is OK if no proxy is needed or has been set through the environment variable HTTPS_PROXY"
        #          , module)

        return messages.message["ok"]
