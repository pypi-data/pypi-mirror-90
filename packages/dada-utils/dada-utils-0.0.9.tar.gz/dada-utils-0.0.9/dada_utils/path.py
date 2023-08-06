"""
Filepath / os utilities
TODO:
    - [ ] Use pathlib instead? https://treyhunner.com/2018/12/why-you-should-be-using-pathlib/
"""

# ///////////////////
# Imports
# ///////////////////

import io
import os
import sys
import json
import pipes
import shutil
import urllib
import hashlib
import tempfile
import mimetypes
import subprocess
from uuid import uuid4
from datetime import datetime
from shutil import copyfile, copy2
from typing import List, Union, Tuple, Any, NewType, Optional

import magic
import checksumdir

import dada_settings


# /////////////
# Custom Types
# /////////////

Filepath = NewType("Filepath", str)  # A filepath string


class PathError(ValueError):
    pass


# ///////////////////
# Reusable Doc Strings
# ///////////////////

PATH_PARAM = ":param path: A filepath as a string"

_mime = magic.Magic(mime=True)

# ///////////////////
# FUNCTIONS
# ///////////////////


def here(fileobj: object, *paths: List[str]) -> str:
    """
    Get the current directory and absolute path of a __file__.
    :param filobj: the ``__file__`` metavar
    :param paths: a list of path sections to pass to ``os.path.join``
    :return str
    """
    return os.path.abspath(os.path.join(os.path.dirname(fileobj), *paths))


def get_full(path: Filepath) -> str:
    f"""
    Get a full path
    {PATH_PARAM}
    :return str
    """
    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = os.path.normpath(path)
    path = os.path.abspath(path)
    return path


def get_relpath(path: Filepath, **kwargs) -> str:
    f"""
    Get a relative path
    {PATH_PARAM}
    :return str
    """
    return os.path.relpath(path, **kwargs)


def get_base_path(path: Filepath) -> str:
    f"""
    Get a filepath's basename with its extension removed
    {PATH_PARAM}
    :return str
    """
    return os.path.basename(path)


def get_name(path: Filepath) -> str:
    f"""
    Get a filepath's basename with its extension (including .gz) removed
    {PATH_PARAM}
    :return str
    """
    base = get_base_path(path)
    ext = get_ext(base)
    if ext:
        return base[: -len(ext) - 1]
    return base


def get_dir(path: Filepath) -> str:
    f"""
    Get a filepath's directory
    {PATH_PARAM}
    :return str
    """
    file_path = get_base_path(path)
    file_dir = path[0 : -(len(file_path))]
    return file_dir


# Extensions + Mimtypes #


def get_ext(path: Filepath, include_gz=True) -> Union[str, None]:
    f"""
    Get a filepath's extension.
    {PATH_PARAM}
    :return str
    """
    _, ext = os.path.splitext(path)
    if not ext:
        return None
    if ext.startswith("."):
        ext = ext[1:]
    if ext == "gz":
        _, new_ext = os.path.splitext(path.replace(".gz", ""))
        if new_ext is not None:
            ext = f"{new_ext}.gz"
            if ext.startswith("."):
                ext = ext[1:]
    return ext.lower()


def get_ungzipped_name(path: Filepath):
    if path.lower().endswith(".gz") or path.lower().endswith(".z"):
        return ".".join(path.split(".")[:-1])
    return path


def get_gzipped_name(path: Filepath):
    if not path.endswith(".gz"):
        path += ".gz"
    return path


def get_mimetype(path: Filepath) -> Union[str, None]:
    f"""
    Guess a file's mimetype given it's path
    {PATH_PARAM}
    :return str
    """
    mt = _mime.from_file(path)
    if mt is not None:
        return mt.lower()
    return None


def get_ext_from_mimetype(mimetype: str) -> Union[str, None]:
    """ Get an ext (`mp3`) from a mimetype `audio/mpeg`"""
    ext = mimetypes.guess_extension(mimetype)
    if ext is not None:
        if ext.startswith("."):
            return ext[1:].lower()
        return ext.lower()
    return None


def get_mimetype_from_ext(ext: str) -> Union[str, None]:
    """ Get a mimetype `audio/mpeg` from and ext (`mp3`)"""
    mt = mimetypes.guess_type(f"file.{ext}")
    if mt is not None:
        return mt.lower()
    return None


def get_ext_and_mimetype(path: Filepath) -> tuple:
    f"""
    dada_settings.FILE_VALID_EXT_MIMETYPE
    dada_settings.FILE_VALID_MIMETYPE_EXT
    """
    # get initial values
    raw_ext = get_ext(path)
    raw_mt = get_mimetype(path)

    # quick check if they are valid
    if (
        raw_ext in dada_settings.FILE_VALID_EXT_MIMETYPE
        and raw_mt in dada_settings.FILE_VALID_MIMETYPE_EXT
    ):
        return raw_ext, raw_mt

    #  try to parse one from the other
    if raw_ext is None and raw_mt is not None:
        raw_ext = get_ext_from_mimetype(raw_mt)

    if raw_mt is None and raw_ext is not None:
        raw_mt = get_mimetype_from_ext(raw_ext)

    # check again if they are valid
    if (
        raw_ext in dada_settings.FILE_VALID_EXT_MIMETYPE
        and raw_mt in dada_settings.FILE_VALID_MIMETYPE_EXT
    ):
        return raw_ext, raw_mt

    # if they are not none return them
    if raw_ext is not None and raw_mt is not None:
        return raw_ext, raw_mt

    if raw_ext is None:
        raw_ext = dada_settings.FILE_DEFUALT_DEFAULT_EXT
    if raw_mt is None:
        raw_mt = dada_settings.FILE_DEFAULT_DEFAULT_MIMETYPE

    return raw_ext, raw_mt


def get_byte_size(path: Filepath) -> int:
    f"""
    Get a filepath's size
    {PATH_PARAM}
    :return int
    """
    return int(os.path.getsize(path))


def get_size(path: Filepath) -> int:
    f"""
    Get a filepath's size
    {PATH_PARAM}
    :return int
    """
    return get_byte_size(path)


def get_check_sum(path: Filepath, block_size: int = io.DEFAULT_BUFFER_SIZE) -> str:
    """
    Get the check sum of a filepath / directory
    """
    if is_dir(path):
        return get_dir_hash(path)
    md5 = hashlib.md5()
    with io.open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            md5.update(chunk)
    return str(md5.hexdigest())


def get_dir_hash(path: Filepath) -> str:
    f"""
    Get a hash of a file / directory's contents
    {PATH_PARAM}
    :return str
    """
    return str(checksumdir.dirhash(path))


def get_path_hash(path: Filepath) -> str:
    f"""
    Get a hash of a filepath
    {PATH_PARAM}
    :return str
    """
    return str(hashlib.md5(path.encode("utf-8")).hexdigest())


IGNORE_PATHS = ["__MACOSX", ".DS_Store"]


def list_files(path: Filepath, ignore_hidden: bool = False) -> List[str]:
    f"""
    Recursively list files under a directory.
    {PATH_PARAM}
    :param ignore_hidden: whether or not to ignore hidden files (starting with ``.``)
    :return list
    """
    return (
        join(dp, f)
        for dp, dn, fn in os.walk(get_full(path))
        for f in fn
        if not (f.startswith(".") and ignore_hidden)
        and not f.endswith(".DS_Store")
        and not dp == "__MACOSX"
    )


def exists(path: Filepath) -> bool:
    f"""
    Check if a filepath exists
    {PATH_PARAM}
    :return bool
    """
    return os.path.exists(path)


def copy(from_path: Filepath, to_path: Filepath) -> None:
    """
    Copy a file from one location to another, ensuring the presence of the target directory.
    """
    from_path = get_full(from_path)
    if is_dir(to_path):
        to_path = make_dir(to_path)
    else:
        make_dir(get_dir(to_path))
    return copyfile(from_path, to_path)


def move(from_path: Filepath, to_path: Filepath) -> None:
    """
    Copy a file from one location to another, ensuring the presence of the target directory, then removing the source file
    """
    copy(from_path, to_path)
    remove(from_path)


def get_created_at(path) -> datetime:
    f"""
    Get the time a file was created as a datetime object
    {PATH_PARAM}
    :return datetime
    """
    return datetime.fromtimestamp(os.path.getctime(path))


def get_updated_at(path) -> datetime:
    f"""
    Get the time a file was last updated as a datetime object
    {PATH_PARAM}
    :return datetime
    """
    return datetime.fromtimestamp(os.path.getmtime(path))


def remove(path: Filepath) -> bool:
    f"""
    Delete a file / directory. Returns True if successful, False if the path does not exist.
    {PATH_PARAM}
    :return bool
    """
    if exists(path):
        if is_dir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return True
    return False


def is_dir(path: Filepath) -> bool:
    f"""
    Check if a path is a directory
    {PATH_PARAM}
    :return str
    """
    return os.path.isdir(path)


def join(*paths: List[str]) -> str:
    f"""
    create a filepath from a list of path parts
    :param paths: A list of path parts
    :return str
    """
    return os.path.join(*paths)


def make_dir(path: Filepath) -> str:
    f"""
    Create a directory
    {PATH_PARAM}
    :return str
    """
    path = get_full(path)
    os.makedirs(path, exist_ok=True)
    return path


def get_env_name(name: str) -> str:
    """
    Get an env var name
    :param name: the env var name
    :return str
    """
    name = name.strip().replace(" ", "_").upper()
    if name.startswith(dada_settings.ENV_VAR_PREFIX):
        return name
    return f"{dada_settings.ENV_VAR_PREFIX}_{name}".upper()


def get_env(name: str, default: Optional[Any] = None) -> Any:
    """
    get env var
    :param name: the env var name
    :return Any
    """
    return os.getenv(get_env_name(name), default)


# ////////////////
# Tempfile utilities
# ////////////////

TEMP_PREFIX = "sickdb-temp"


def get_tempdir() -> str:
    """
    Create a temporary directory
    :return str
    """
    if dada_settings.TEMPFILE_DIR:
        return dada_settings.TEMPFILE_DIR
    return tempfile.mkdtemp(prefix=TEMP_PREFIX)


def get_tempfile(name: Optional[str] = None, ext: Optional[str] = None) -> str:
    """
    Create a tempfile with a custom name and extension
    :param name: The file name
    :param ext: The file extension
    :return str
    """
    # attempt to format name / ext automatically
    if name:
        name = get_name(name)
        if not ext:
            ext = get_ext(name)

    if not name:
        name = f"{uuid.uuid4()}"

    if not ext:
        ext = "tmp"

    return join(get_tempdir(), f"{name}.{ext}")


def get_tempfile_from_fobj(
    fobj: object, name: Optional[str] = None, ext: Optional[str] = None
) -> str:
    """
    Given a file-like obj, write to a temp field with a custom name, and return filepath
    :param fobj: A file-like object
    :param name: The file name
    :param ext: The file extension
    :return str
    """
    tmp_path = get_tempfile(name or getattr(fobj, "filename", None), ext)
    with open(tmp_path, "wb") as f:
        f.write(fobj.read())
    fobj.close()
    return tmp_path


class Process(object):
    """
    A class for running a subprocess
    :param command: A command to run.
    """

    def __init__(self, command: str):
        self.command = command
        self._stdin = None
        self._stdout = None
        self._stdout_text = None
        self._returncode = None

    def set_stdin(self, stdin):
        self._stdin = stdin

    def set_stdout(self, stdout):
        self._stdout = stdout

    @property
    def stdin(self):
        return "stdin"

    @property
    def stdout(self) -> Union[None, str]:
        if self._stdout_text is not None:
            return self._stdout_text

    @property
    def json(self) -> Union[None, str]:
        if self.stdout is not None:
            return json.loads(self._stdout_text)

    @property
    def stderr(self) -> Union[None, str]:
        if self._stderr_text is not None:
            return self._stderr_text

    @property
    def returncode(self):
        if self._returncode is not None:
            return self._returncode

    @property
    def ok(self):
        if self._returncode is not None:
            return self.returncode == 0

    @property
    def subprocess(self):
        if self._subprocess is not None:
            return self._subprocess

    def start(self):
        self._subprocess = subprocess.Popen(
            args=self.command,
            shell=True,
            stdin=self._stdin if self._stdin else subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

    def wait(self, unread=False):
        self._returncode = self._subprocess.wait()
        if self._subprocess.stdout is not None and not unread:
            self._stdout_text = self._subprocess.stdout.read().decode()
            self._stderr_text = self._subprocess.stderr.read().decode()

    def run(self):
        self.start()
        self.wait()

    def __repr__(self):
        return "<Process: {0}>".format(self.command)


def exec(cmd: str) -> Process:
    """
    Run a shell command.
    """
    p = Process(cmd)
    p.run()
    return p


def get_exec_path(prog: str) -> Union[str, None]:
    """
    Get an executable path given a program name
    :param prog: A program to look for (eg: ``jq``)
    :return str, None
    """
    for p in os.environ["PATH"].split(os.pathsep):
        fullpath = os.path.join(p, prog)
        if os.access(fullpath, os.X_OK):
            return fullpath
