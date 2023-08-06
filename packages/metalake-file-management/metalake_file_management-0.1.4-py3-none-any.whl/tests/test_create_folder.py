import pytest
from src.adls_management import folder_management


def test_create_folder():
    folder_management.ADLSFolderManagement().create_directory("test")
