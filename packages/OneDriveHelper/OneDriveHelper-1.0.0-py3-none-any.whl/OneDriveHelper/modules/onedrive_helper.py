import ntpath
import os

from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.files.file import File
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from OneDriveHelper.exceptions.OneDriverExceptions import DownloadError, Error, DeleteError


class OneDriverHelper:

    def __init__(self, base_url: str, client_id: str, client_secret: str, site_name: str, folder_name: str = None,
                 root_title="Documents"):
        """
        This class have operations that can upload, get and delete to Sharepoint
        :param base_url: site name like https://channelcapitalcouk.sharepoint.com
        :type base_url: str
        :type client_id: str
        :type client_secret: str
        :param site_name: SharePoint site name
        :type site_name: str
        :param folder_name: Folder name on the SharePoint
        :type folder_name: str
        """
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.site_name = site_name
        self.folder_name = folder_name
        self.root_title = root_title

        self._credentials = ClientCredential(self.client_id, self.client_secret)
        self._ctx = ClientContext(self.base_url + '/sites/' + self.site_name).with_credentials(self._credentials)
        self._web = self._ctx.web
        self._ctx.execute_query()
        self._root_folder = self._web.lists.get_by_title(self.root_title).rootFolder

    def download_file(self, file: File, download_path="../"):
        """
        Download file to given path
        :param file:
        :type file: office365.sharepoint.files.file.File
        :param download_path:
        :type download_path: str
        :return: information about result
        :rtype: str
        """
        try:
            with open(f"{download_path}/{file.properties['Name']}", 'wb') as ftd:
                self._ctx.web.get_file_by_server_relative_url(file.properties['ServerRelativeUrl']).download(
                    ftd).execute_query()
            return f"{file.properties['Name']} downloaded to {download_path}"
        except ClientRequestException as err:
            raise DownloadError(err)
        except Exception as err:
            raise Error(err)

    def get_list_of_files(self, folder=None):
        """
        Gives list of files either in the root folder or given folder
        :param folder:
        :type folder:
        :return: None or information about error
        :rtype:
        """
        list_of_files = []
        if folder is not None:
            try:
                active_folder = self.set_active_folder(folder)
                files = active_folder.files
                self._ctx.load(files)
                self._ctx.execute_query()
            except Exception as err:
                return f"Something went wrong {err}"
        else:
            try:
                files = self._root_folder.files
                self._ctx.load(files)
                self._ctx.execute_query()
            except Exception as err:
                return f"Something went wrong {err}"

        for file in files:
            list_of_files.append(file)

        return list_of_files

    def upload_file(self, file_name, context, folder=None):
        """
        Upload a file to root folder or given folder
        :param file_name:
        :type file_name: str
        :param context:
        :type context: binary
        :param folder:
        :type folder: str
        :return: information about result
        :rtype: str
        """
        if folder is None:
            try:
                self._root_folder.upload_file(file_name, context).execute_query()
                return f"{file_name} uploaded to {self.base_url}"
            except Exception as err:
                return f"Something went wrong {err}"
        else:
            try:
                active_folder = self.set_active_folder(folder)
                active_folder.upload_file(file_name, context).execute_query()
                return f"{file_name} uploaded to {self.base_url}/{folder}"
            except Exception as err:
                return f"Something went wrong {err}"

    def upload_file_from_path(self, path, upload_folder=None):
        head, tail = ntpath.split(path)
        with open(path, 'rb') as file:
            return self.upload_file(tail.decode('ascii'), file.read(), upload_folder)

    def delete_file(self, file: File):
        """
        Delete given file from SharePoint sites
        :param file:
        :type file:  office365.sharepoint.files.file.File
        :return: Information about operation
        :rtype: str
        """
        try:
            self._ctx.web.get_file_by_server_relative_url(
                file.properties['ServerRelativeUrl']).delete_object().execute_query()
            return f"{file.properties['Name']} has been deleted from {self.base_url}"
        except ClientRequestException as err:
            raise DeleteError(err)
        except Exception as err:
            raise Error(err)

    def set_active_folder(self, folder):
        """Set active folder to download, delete or upload."""
        return self._ctx.web.get_folder_by_server_relative_url(
            f"/sites/{self.site_name}/{self.root_title}/{folder}")

    def download_all(self, folder=None, download_path=None):
        """
        Loop through files in the folder and download all
        :param folder:
        :type folder:
        :param download_path:
        :type download_path:
        :return:
        :rtype:
        """
        files = self.get_list_of_files(folder)
        for f in files:
            self.download_file(f, download_path=download_path)
        return f"Files in folder {self.site_name}/{folder} has been downloaded tho folder {download_path}"


    def delete_all(self, folder=None):
        """
        Loop through files in the folder and delete all
        :param folder:
        :type folder:
        :return:
        :rtype:
        """
        files = self.get_list_of_files(folder)
        if len(files) == 0:
            return f"Folder is empty"

        for f in files:
            self.delete_file(f)
        return f"Files in folder {self.site_name}/{folder} has been deleted"

    def upload_all(self, folder=None, folder_path='./'):
        """
        Loop through files in the folder and upload all
        :param folder:
        :type folder:
        :param folder_path:
        :type folder_path:
        :return:
        :rtype:
        """
        directory = os.fsencode(folder_path)
        files = os.listdir(directory)
        for f in files:
            file_name = os.fsencode(f)
            self.upload_file_from_path(os.path.join(directory, file_name), folder)
        return f"All files in {folder_path} uploaded to"
