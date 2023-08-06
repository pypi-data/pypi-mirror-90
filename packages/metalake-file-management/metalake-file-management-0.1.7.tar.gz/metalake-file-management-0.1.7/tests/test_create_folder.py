from metalake_management.adls_management import folder_management


def test_create_folder():
    folder_management.ADLSFolderManagement("tests/resources/connection_config.json").create_directory("test")
