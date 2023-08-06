"""
Archive extraction via patool / zipfile. 
TODO:
    - [ ] Remove dependence on `patool` and only use specific archive formats?.
"""

# ///////////////////
# Imports
# ///////////////////


import logging
import sys
import zipfile
from typing import Optional, List

import patoolib

from dada_utils import path


# ///////////////////
# Logger
# ///////////////////

ARCHIVE_LOGGER = logging.getLogger()

# ///////////////////
# Custom Types
# ///////////////////
class ArchiveError(ValueError):
    pass


# ///////////////////
# Doc strings
# ///////////////////
FILENAME_PARAM = ":param filename: str filename to extract"
BACKEND_PARAM = ":param backend: ``auto``, ``patool`` or ``zipfile``"
DIRECTORY_PARAM = ":param directory: directory to extract to"
VERBOSE_PARAM = ":param verbose: bool whether or not to log patool output"
PATOOL_PATH_PARAM = ":param patool_path: (Optional) path to to patool executable"
IGNORE_HIDDEN_PARAM = ":param ignore_hidden: ignore hidden files (startswith .)"


def extract_all(
    filename: str,
    directory: Optional[str] = None,
    backend: str = "auto",
    verbose: bool = False,
    ignore_hidden: bool = True,
    **kwargs,
) -> List[str]:
    f"""
    General purpose archive extraction via `patool` + `zipfile`
    {FILENAME_PARAM}
    {DIRECTORY_PARAM}
    {BACKEND_PARAM}
    {VERBOSE_PARAM}
    {PATOOL_PATH_PARAM}
    {IGNORE_HIDDEN_PARAM}
    :return list
    """
    ar = Archive(filename, backend, verbose)
    return ar.extract_all(
        directory=directory, backend=backend, ignore_hidden=ignore_hidden
    )


class Archive(object):
    f"""
    {FILENAME_PARAM}
    {BACKEND_PARAM}
    {VERBOSE_PARAM}
    """
    __module__ = "dada_utils.archive"

    def __init__(self, filename: str, backend: str = "auto", verbose: bool = False):
        self.filename = path.get_full(filename)
        self.backend = backend
        self.verbose = verbose

    def extract_all_patool(self, directory: str,) -> None:
        f"""
        Extract all files in an archive via ``patool``
        {DIRECTORY_PARAM}
        :return None
        """
        ARCHIVE_LOGGER.debug("starting backend patool")
        patoolib.extract_archive(
            self.filename, verbosity=self.verbose, interactive=False, outdir=directory
        )

    def extract_all_zipfile(self, directory: str) -> None:
        f"""
        Extract all files in an archive via ``zipfile``
        {DIRECTORY_PARAM}
        :return None
        """
        ARCHIVE_LOGGER.debug("starting backend zipfile")
        zipfile.ZipFile(self.filename).extractall(directory)

    def extract_all(
        self,
        directory: Optional[str] = None,
        backend: Optional[str] = None,
        ignore_hidden: bool = True,
    ) -> List[str]:
        f"""
        Extract files in an archive via patool / zipfile.
        {DIRECTORY_PARAM}
        {PATOOL_PATH_PARAM}
        {IGNORE_HIDDEN_PARAM}
        """
        ARCHIVE_LOGGER.debug(
            "extracting %s into %s (backend=%s)", self.filename, directory, backend
        )
        if backend:
            self.backend = backend

        # create the directory
        if not directory:
            directory = path.get_tempdir()

        directory = path.get_full(directory)

        if not path.exists(self.filename):
            raise ArchiveError("archive file does not exist:" + str(self.filename))

        elif not directory or not path.exists(directory) or not path.is_dir(directory):
            raise ArchiveError(
                "output directory does not exist: {directory}" + str(directory)
            )

        is_zipfile = zipfile.is_zipfile(self.filename)
        if backend == "auto":
            if is_zipfile:
                self.extract_all_zipfile(directory)
            else:
                self.extract_all_patool(directory)

        if backend == "zip":
            if not is_zipfile:
                raise ValueError("[archive] file is not zip file:" + str(self.filename))
            self.extract_all_zipfile(directory)

        if backend == "patool":
            self.extract_all_patool(directory)

        # return the list of files
        return list(path.list_files(directory, ignore_hidden=ignore_hidden))
