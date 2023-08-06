import os
import shutil
import tempfile

import pytest

from OneDriveHelper.modules import OneDriverHelper
from OneDriveHelper.config import config
from OneDriveHelper.exceptions.OneDriverExceptions import DownloadError, DeleteError


class TestOneDriver:
    def setup(self):
        self.config = config().config
        credentials = self.config['credentials']
        self.onedriver = OneDriverHelper(base_url=credentials['base_path'],
                                         client_id=credentials['client_id'],
                                         client_secret=credentials['client_secret'],
                                         site_name=credentials['site_name'],
                                         root_title=credentials['root_title']
                                         )

    def test_get_list_of_files(self):
        assert type(self.onedriver.get_list_of_files()) is list

        print()
        for file in self.onedriver.get_list_of_files():
            print(file.properties['Name'])

    def test_download_error(self):
        with pytest.raises(DownloadError):
            files = self.onedriver.get_list_of_files()
            files[0].properties['ServerRelativeUrl'] = "aaaaaa"
            self.onedriver.download_file(files[0], "/Volumes/Working Blue/Channels/PythonWorks/OneDriveHelper/test/test_files")

    def test_delete_file_error(self):
        with pytest.raises(DeleteError):
            files = self.onedriver.get_list_of_files()
            files[0].properties['ServerRelativeUrl'] = "aaaaaa"
            self.onedriver.delete_file(files[0])

    def test_download_file(self):
        files = self.onedriver.get_list_of_files()

        self.onedriver.download_file(files[0], "/test/test_files")
        a = self.temp_download(files[0].properties['ServerRelativeUrl'], files[0].properties['Name'])

        with open(f"./test_files/{files[0].properties['Name']}", 'rb') as file:
            assert a.read() == file.read()

        os.remove(f"./test_files/{files[0].properties['Name']}")



    def test_download_all(self):
        self.onedriver.download_all(folder='/test', download_path='/test/test_download')

        files, file_names = self.get_files_and_file_names(folder='/test')
        local_files = set(os.listdir('test_download'))
        file_names = set(file_names)

        assert local_files == file_names

        self.delete_files_in_folder('test_download')

    def test_upload_and_delete_file(self):
        ### Upload
        with open("test_files/0o0Ii1A3tKml.txt", 'rb') as ftu:
            self.onedriver.upload_file("0o0Ii1A3tKml.txt", ftu.read())

        files, file_names = self.get_files_and_file_names()
        assert "0o0Ii1A3tKml.txt" in file_names
        ### Delete
        for f in files:
            if f.properties['Name'] == "0o0Ii1A3tKml.txt":
                self.onedriver.delete_file(f)
        files, file_names = self.get_files_and_file_names()
        assert "0o0Ii1A3tKml.txt" not in file_names

    def test_upload_and_delete_file_with_folder(self):
        ### Upload
        with open("test_files/0o0Ii1A3tKml.txt", 'rb') as ftu:
            self.onedriver.upload_file("0o0Ii1A3tKml.txt", ftu.read(), folder='test')

        test_files, test_file_names = self.get_files_and_file_names(folder='test')
        assert "0o0Ii1A3tKml.txt" in test_file_names
        ### Delete
        for f in test_files:
            if f.properties['Name'] == "0o0Ii1A3tKml.txt":
                self.onedriver.delete_file(f)
        test_files, test_file_names = self.get_files_and_file_names(folder='test')
        assert "0o0Ii1A3tKml.txt" not in test_file_names

    def test_delete_file(self):
        self.onedriver.upload_file_from_path("test_files/0o0Ii1A3tKml.txt")

        files = self.onedriver.get_list_of_files()
        for file in files:
            if file.properties['Name'] == '0o0Ii1A3tKml.txt':
                self.onedriver.delete_file(file)

        files, file_names = self.get_files_and_file_names()
        assert '0o0Ii1A3tKml.txt' not in file_names

    def test_delete_and_update_all(self):
        """
        Looks for the test folder, if there are any files deletes them, else upload files from test_files local
        folder
        :return:
        :rtype:
        """
        files, file_names = self.get_files_and_file_names(folder='test')
        if len(files) > 0:
            self.onedriver.delete_all('/test')
        else:
            ### Update_all test
            self.onedriver.upload_all(folder='test', folder_path='test_files')
            files, file_names = self.get_files_and_file_names(folder='test')
            assert len(files) > 0

            self.onedriver.delete_all('/test')

        files, file_names = self.get_files_and_file_names(folder='test')
        assert len(files) == 0

    def temp_download(self, server_relative_url, file_name):
        download_path = os.path.join(tempfile.mkdtemp(), os.path.basename(file_name))
        with open(download_path, "wb") as local_file:
            file = self.onedriver._ctx.web.get_file_by_server_relative_url(server_relative_url).download(
                local_file).execute_query()
        return file

    def get_files_and_file_names(self, folder=None):
        files = self.onedriver.get_list_of_files(folder)
        file_names = list(map(lambda x: x.properties['Name'], files))
        return files, file_names

    @staticmethod
    def delete_files_in_folder(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as err:
                print(f"Failed to delete {file_path}. Reason: {err}")
