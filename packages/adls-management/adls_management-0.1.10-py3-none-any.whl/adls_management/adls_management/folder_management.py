from adls_management.adls_management import connection
from adls_management.utils import settings, messages


class ADLSFolderManagement:

    def __init__(self, configuration_file):
        # use provided connection config file
        self.settings = settings.GenericSettings(configuration_file=configuration_file)
        self.settings.get_config()

        self.service_client, self.file_system_client, self.blob_service_client, self.container_client, self.sas_token \
            = connection.ConnectionManagement(self.settings).create_connection(
            storage_account_name=self.settings.storage_account_name
            , storage_account_key=self.settings.storage_account_key
            , container=self.settings.storage_container
        )

    def create_directory(self, directory):
        try:
            self.file_system_client.create_directory(directory=directory)
        except Exception as e:
            print(e)
            return messages.message["directory_creation_error"]
        return messages.message["ok"]

    def delete_directory(self, directory):
        try:
            self.file_system_client.delete_directory(directory=directory)
        except Exception as e:
            print(e)
            return messages.message["directory_removal_error"]
        return messages.message["ok"]
