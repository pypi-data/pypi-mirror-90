from metalake_management.utils import messages
from metalake_management.interface_file_management import interface_file_handling
from datetime import datetime, date
from uuid import uuid4
from metalake_management.adls_management import folder_management
from os import path


class FilesBatchPhaseFromTo:
    """
        Convenience modules to move files from one stage to the next.
        locations need to be configured in resources/locations.json (default)
    """
    right_now = datetime.now().isoformat(timespec="microseconds").replace(":", "-")
    # todays_date = datetime.today().strftime("%Y-%m-%d")

    def __init__(self, configuration_file, run_id=None):
        self.run_id = None
        self.run_id, self.time_id = self.determine_run_id()
        print("run_id is >%s< with time_stamp >%s<" % (self.run_id, self.time_id))
        self.result = messages.message["ok"]
        self.file_handler = interface_file_handling.InterfaceFileHandling(configuration_file=configuration_file)
        self.mgmt = folder_management.ADLSFolderManagement(configuration_file=configuration_file)
        self.container_handler = self.mgmt.container_client
        self.oldest_name = None

    def determine_run_id(self):
        if self.run_id is None:
            the_run_id = str(uuid4())
        else:
            the_run_id = self.run_id
        return the_run_id, self.right_now

    def determine_target_name(self, base_name):
        return path.join(base_name, self.right_now + "--" + self.run_id)

    def determine_oldest_folder(self, base_folder):
        # given the fact that this code also created the folder structure:
        # all folders have timestamp(formatted)+ '--' + uuid4
        # NOTE: A directory is listed by name on Azur Blobs, so actually the first one found is the oldest,
        #       given the naming convention of this tooling
        # print("content of %s:" % base_folder)
        oldest_name = "not_found"
        # introduce the year 3030 problem:
        oldest = 30301224093810129694
        result, sources, source_names = self.file_handler.list_files(location=base_folder, file_pattern="*")
        # for folder in self.container_handler.walk_blobs(base_folder, delimiter='/'):
        for folder in source_names:
            # print(folder)
            if "--" not in folder:
                # print(">%s< is not a file we are interested in" % folder)
                continue
            time_from_name = folder.split("--")[0]
            file_nr_as_str = ''.join(c for c in time_from_name if c.isdigit())
            # print("file >%s< has timestamp >%s< which is >%s<" % (folder, time_from_name, file_nr_as_str))
            if file_nr_as_str == "":
                self.oldest_name = "not_found"
            else:
                file_nr = int(file_nr_as_str)
                if file_nr < oldest:
                    self.oldest_name = folder
                    oldest = file_nr

        return oldest, self.oldest_name

    def from_incoming2todo(self):
        """
            Move the files to 'todo' so they can be processed. The 'incoming' is freed-up for new files.
        """
        print("=== from_incoming2todo ===")
        result = self.from_to(self.file_handler.settings.incoming, self.file_handler.settings.todo)
        result["reference"] = "from >%s< to >%s<" % (self.file_handler.settings.incoming, self.file_handler.settings.todo)
        return result

    def from_todo2busy(self):
        """
            Move the files to 'busy' as pre-processing step of the actual processing
            Move the files from the oldest folder to the 'busy' folder
            Note: In this release, we cannot have multiple processes processing files.
                The 'busy' folder can only contain one single set of files
        """
        # find the oldest folder
        print("=== from_todo2busy ===")
        from_folder = self.file_handler.settings.todo
        print("from_folder is >%s<" % from_folder)
        oldest, self.oldest_name = self.determine_oldest_folder(base_folder=from_folder)
        print("oldest_folder is >%s<" % self.oldest_name)
        if self.oldest_name == "not_found" or self.oldest_name == "" or self.oldest_name is None:
            result = messages.message["could_not_determine_oldest_folder"]
            return result

        # to_work_on_folder = oldest_name.split('/')[1]
        target = self.file_handler.settings.busy
        result = self.from_to(path.join(from_folder, self.oldest_name), target)
        if result["code"] == "OK":
            result["reference"] = "oldest_name >%s< went to >%s<" % (self.oldest_name, target)
        if result["code"] == "MLU-FH-009":
            # empty source folder
            result = self.mgmt.create_directory(path.join(self.file_handler.settings.done, self.oldest_name))
            if result["code"] == "OK":
                result = self.mgmt.delete_directory(directory=path.join(self.file_handler.settings.todo, self.oldest_name))
        return result

    def from_busy2done(self):
        print("=== from busy2done ===")
        from_folder = path.join(self.file_handler.settings.busy, self.oldest_name)
        to_folder = path.join(self.file_handler.settings.done, self.oldest_name)
        print("from >%s< to >%s<" % (from_folder, to_folder))
        result = self.from_to(from_location=from_folder, to_location=to_folder)
        return result

    def from_done2hist(self):
        """
            Moves files from 'done' to 'hist', where 'hist' could be a cold location
            Use this on a regular basis to clean-up the 'done' folder
        """
        print("=== from done2hist ===")
        result = self.from_to(self.file_handler.settings.done, self.file_handler.settings.hist)
        return result

    def from_busy2redo(self):
        """
            When an error occurred use this method to move the files to the configured 'redo'
        """
        print("=== from busy2redo ===")
        result = self.from_to(self.file_handler.settings.busy, self.file_handler.settings.redo)
        return result

    def from_to(self, from_location, to_location):
        """
            Move files from the configured from_location to the configured to_location (check locations.json)
        """
        print("--- from_to ---")
        result, files, file_names = self.file_handler.list_files(location=from_location, file_pattern="*")
        if result["code"] == "OK":
            if len(files) > 0:
                target_directory = self.determine_target_name(to_location)
                result = self.mgmt.create_directory(directory=target_directory)
                if result["code"] == "OK":
                    result = self.free_from_to(from_location=from_location, to_location=target_directory)
            else:
                print("No files in source:", from_location)
                result = messages.message["no_files_in_source"]
        return result

    def free_from_to(self, from_location, to_location):
        """
        """
        print("free - from >%s< to >%s<" % (from_location, to_location))
        result = self.file_handler.move_files(from_location=from_location
                                                  , to_location=to_location
                                                  , file_pattern="*")
        return result
