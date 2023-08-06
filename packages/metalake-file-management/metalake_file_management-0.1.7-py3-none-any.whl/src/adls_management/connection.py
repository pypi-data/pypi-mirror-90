import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from metalake_management.utils import settings
from azure.storage.blob import BlobClient, BlobServiceClient, generate_account_sas
from azure.storage.blob import ResourceTypes, AccountSasPermissions
from datetime import datetime, timedelta


class ConnectionManagement:

    def __init__(self, settings):
        self.service_client = None
        self.file_system_client = None
        self.settings = settings
        self.blob_service_client = None
        self.container_client = None
        self.sas_token = None

    def create_connection(self, storage_account_name, storage_account_key, container):
        try:
            dfs_url="{}://{}.dfs.core.windows.net".format("https", storage_account_name)
            blob_url="{}://{}.blob.core.windows.net/".format("https", storage_account_name)
            # print("ADLS URL:", dfs_url)
            # print("Blob URL:", blob_url)
            self.service_client = DataLakeServiceClient(account_url=dfs_url, credential=storage_account_key)
            # print("Getting file_system_client...")
            self.file_system_client = self.service_client.get_file_system_client(
                file_system=self.settings.storage_container
            )
            # print("Getting blob_service_client...")
            connect_string="DefaultEndpointsProtocol=https;AccountName=" + storage_account_name + ";AccountKey="\
                           + storage_account_key + ";EndpointSuffix=core.windows.net"
            self.blob_service_client = BlobServiceClient.from_connection_string(
                    conn_str=connect_string)
            # Create sas token for blob

            self.sas_token = generate_account_sas(
                account_name=self.blob_service_client.account_name,
                account_key=storage_account_key,
                resource_types = ResourceTypes(service=True, object=True, container=True),
                permission = AccountSasPermissions(read=True, write=True, delete=True, list=True, add=True, create=True),
                start = datetime.now() - timedelta(hours=1),
                expiry = datetime.utcnow() + timedelta(hours=4)  # Token valid for 4 hours
            )
            self.container_client = self.blob_service_client.get_container_client(container)
            # print("returning references.")
            return self.service_client\
                , self.file_system_client\
                , self.blob_service_client\
                , self.container_client\
                , self.sas_token

        except Exception as e:
            print(e)
            return None, None, None, None, None
