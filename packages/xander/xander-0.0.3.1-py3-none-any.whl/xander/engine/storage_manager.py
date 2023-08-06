import glob
import os
import re
from os.path import sep
import geopandas as gpd

import pandas as pd
from zipfile import ZipFile
from fiona.errors import DriverError


def read_file(folder, filename, version):
    """
    Search in the folder the file and retrieve the specified version.
    """

    latest_version_filter = find_last_version(folder=folder, filename=filename)

    fixed_filename = filename

    if latest_version_filter:
        fixed_filename = os.path.join(sep.join(filename.split(sep)[:-1]),
                                      filename.split(sep)[-1].split('.')[0] + '_v{}.'.format(
                                          latest_version_filter) + filename.split(sep)[-1].split('.')[1])

    path = os.path.join(folder, fixed_filename)
    if filename.endswith('.csv'):
        return pd.read_csv(path, sep=';')
    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        return pd.read_excel(path)
    elif filename.endswith('.shp'):
        return gpd.read_file(path)
    elif filename.endswith('.zip'):
        return ZipFile(path, 'r')

    return None


def validate_path(folder, force, logger):
    """
    Check if the path points to a folder and validates it.

    :param folder: path to be validated.
    :param force: force to create the folder.
    :param logger: logger object.
    :return: None
    """

    # Check if the path is a folder path or a file path.
    if '.' in folder.split(os.sep)[-1]:
        logger.log("'{}' is file path, please provide a folder path.".format(folder), terminate=True)

    # Check if the path exists.
    if not os.path.isdir(folder):

        # If the force flag is not set, the execution terminates.
        if not force:
            logger.log("'{}' is not a valid path.".format(folder), terminate=True)

        # The folder is created.
        os.mkdir(path=folder)

    return None


def find_last_version(folder, filename):
    """
    Retrieve the latest version of the filename in the folder.

    :param folder: where the file is searched
    :param filename: filename to find the version
    :return: latest version
    """

    filename_without_extension = filename.split(sep)[-1].split('.')[0]
    path_appendix = sep.join(filename.split(sep)[:-1])

    # Use a regex to find the files that are compatible with the filename
    file_list = glob.glob(rf'{os.path.join(folder, path_appendix, filename_without_extension)}_v*')

    # Extract from the name of the file the version and create an array of versions
    versions = [int(re.search('_v(\d+).', file).group(1)) for file in file_list]

    # Sort the array version
    versions = sorted(versions)

    # The last version is the last item in the array of versions otherwise None
    last_version = versions[-1] if versions else None

    return last_version


class StorageManager:

    def __init__(self, local_source, local_destination, logger):

        validate_path(folder=local_source, force=True, logger=logger)
        validate_path(folder=local_destination, force=True, logger=logger)

        self.logger = logger
        self.local_source = local_source
        self.local_destination = local_destination

        self.logger.info('Local source folder: {}'.format(local_source))
        self.logger.info('Local destination folder: {}'.format(local_destination))

    def get_file(self, filename, version='latest'):
        """
        Return (if exists) the file corresponding to the filename in input. Zoe selects
        automatically the version you need, otherwise return the latest one.

        :param filename: name of the file to be loaded
        :param version: version of the file to be loaded
        :return: file content
        """

        try:
            return read_file(folder=self.local_source, filename=filename, version=version)
        except FileNotFoundError:
            return read_file(folder=self.local_destination, filename=filename, version=version)
        except DriverError:
            return read_file(folder=self.local_destination, filename=filename, version=version)

    def export(self, outputs, output_names):
        if isinstance(outputs, tuple) or isinstance(outputs, list):
            for i, output in enumerate(outputs):
                self.export_output(output, output_names[i])
        else:
            self.export_output(outputs, output_names[0])

    def export_output(self, output, output_name):
        """
        Export the ouput from the function of the component.

        :param output_name: name of the output file
        :param output: output object
        :return: None
        """

        latest_version_filter = find_last_version(folder=self.local_destination, filename=output_name)

        if latest_version_filter is not None and latest_version_filter >= 0:
            latest_version_filter += 1
            fixed_filename = output_name.split('.')[0] + '_v{}.csv'.format(latest_version_filter)
        else:
            fixed_filename = output_name.split('.')[0] + '_v0.csv'

        path = os.path.join(self.local_destination, fixed_filename)
        # DataFrame case
        if isinstance(output, pd.DataFrame):
            output.to_csv(path, sep=';', index=False)
            self.logger.success('Exported dataset \'{}\' in \'{}\'.'.format(fixed_filename, self.local_destination))

        # All other cases
        else:
            self.logger.info('Output format not supported yet!')
