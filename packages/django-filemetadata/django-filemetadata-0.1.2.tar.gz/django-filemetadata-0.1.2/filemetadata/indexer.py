import datetime
from pathlib import Path
import os
from django.conf import settings

from filemetadata.models import FileMetadata
from filemetadata.utils import human_readable_size
from filemetadata.utils import is_binary_string
from tzlocal import get_localzone
import logging

logger = logging.getLogger("django-filemetadata")

try:
    import PyPDF4

    PYPDF4_LOADED = True
except ImportError:
    PYPDF4_LOADED = False
    logger.warn("PyPDF4 library not installed. It'll not possible to extract the text from '.pdf' files")


def func_extract_text(file_obj):
    out = ""
    with file_obj.open(mode='rb') as file_data:
        if file_obj.suffix == '.pdf':
            if PYPDF4_LOADED:
                lines = []
                pdf = PyPDF4.PdfFileReader(file_data)
                for num_page in range(0, pdf.getNumPages()):
                    lines.append(pdf.getPage(num_page).extractText())
                out = "\n".join(lines)
        else:
            if not is_binary_string(file_data.read(1024)):
                # Try to index all file in txt format.
                file_data.seek(0)
                out = file_data.read()
    return out


class FileIndexer(object):

    def extract_text(self, file_obj):
        """
        Extract the text from the file object
        :param file_obj: file object
        :return: text content
        """
        return self.sanitize_text(func_extract_text(file_obj))

    @staticmethod
    def sanitize_text(txt):
        """
        Converto to utf-8 and remove unnecessary data and empty lines.
        :param txt: text
        :return: compact text (utf-8)
        """
        txtout = []
        if type(txt) == bytes:
            txt = txt.decode("utf-8", "replace")
        for line in txt.replace(u"\xa0", " ").split("\n"):
            line = line.strip()
            if line:
                txtout.append(line)
        return "\n".join(txtout)

    def normalize_dirs(self, dirs):
        if not dirs:
            dirs = settings.FILEMETADATA_LOOKUP_DIRS
        if not dirs:
            raise FileNotFoundError("Please informe the folder(s) to index or "
                                    "configure FILEMETADATA_LOOKUP_DIRS in the settings.")

        ret = []
        if not isinstance(dirs, (list, tuple)):
            dirs = dirs.split(";")
        for d in dirs:
            error = ''
            d = os.path.abspath(d.strip())
            if os.path.exists(d):
                if os.path.isdir(d):
                    ret.append(d)
                else:
                    error = "'%s' is not a directory." % d
            else:
                error = "'%s' does not exists." % d

            if error:
                if self.raise_errors:
                    raise FileNotFoundError(error)
                else:
                    self.errors.append(error)
        return ret

    def __init__(self, follow_symlinks=True, extract_content=False, recursive=True, raise_errors=False,
                 verbose_print=False):
        """
        Look for files in the filessystem, extract the metadata and save into the DB.

        :param follow_symlinks: follow the symlinks
        :param extract_content: try to get the content of the file in text format.
        :param recursive: search the file recursively in the directories
        :param recursive:
        """
        self.follow_symlinks = follow_symlinks
        self.extract_content = extract_content
        self.recursive = recursive
        self.raise_errors = raise_errors
        self.verbose_print = verbose_print
        self.errors = []
        self.count_added = 0
        self.count_updated = 0
        self.count_deleted = 0

    def retrieve_metadata_file(self, file_obj):
        """
        This method return the metadata from the file.

        :param file_obj: The file (PosixPath object)
        :return: dictionary with the metadata
        """

        filename = file_obj.name
        # TODO: Add follow_symlinks?
        stat = file_obj.stat()
        fpath = os.path.abspath(os.path.dirname(file_obj))
        local = get_localzone()

        content_txt = ""
        if self.extract_content:
            try:
                content_txt = self.extract_text(file_obj)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                if self.raise_errors:
                    raise
                else:
                    self.errors.append("Error extracting the text from file '%s'. %s" % (filename, e))

        return {'file': file_obj,
                'suffix': file_obj.suffix,
                'inode': stat.st_ino,
                'filename': filename,
                'path': fpath,
                'size': stat.st_size,
                'size_str': human_readable_size(stat.st_size),
                'created': datetime.datetime.fromtimestamp(stat.st_ctime, tz=local),
                'modified': datetime.datetime.fromtimestamp(stat.st_mtime, tz=local),
                'title': filename,
                'text_content': content_txt
                }

    def retrieve_metadata_files(self, dirs_str):
        """
        This method return all metadata from the files found in the directories.

        :param dirs_str: list of directories. eg. ['/var/folder1','/var/folder2',]
        :return: list (dictionary) with all metadata.
        """

        def print_indented(obj, prefix, level):
            if self.verbose_print:
                print('  ' * level + prefix + obj)

        def retrieve_folder(dir_obj, level=0, rec=True):
            print_indented(dir_obj.name, '= ', level)
            output = []

            if dir_obj.exists():
                for element in dir_obj.iterdir():
                    if element.is_dir():
                        if rec:
                            output += retrieve_folder(element, level=level + 1)
                    else:
                        try:
                            output.append(self.retrieve_metadata_file(element))
                        except KeyboardInterrupt:
                            raise
                        except Exception as e:
                            if self.raise_errors:
                                raise
                            else:
                                self.errors.append("Error extracting metadata from file %s - %s" % (element.name, e))

                        print_indented(element.name, '- ', level + 1)
            else:
                if self.raise_errors:
                    raise FileNotFoundError("'%s' not found" % dir_obj.name)
                else:
                    self.errors.append("'%s' not found" % dir_obj.name)
            return output

        files = []
        dirs_str = self.normalize_dirs(dirs_str)
        for dir_str in dirs_str:
            directory = Path(dir_str.strip())
            files += retrieve_folder(directory, rec=self.recursive)
        return files

    def delete_metadata_db(self, dirs_str=None):
        """
        Delete the data from the DB with the specific folders (path)
        :param dirs_str: directories to delete
        :return: Number of deleted records
        """
        dirs_str = self.normalize_dirs(dirs_str)
        c = 0
        for dir_str in dirs_str:
            dir_str = dir_str.strip()

            if self.recursive:
                pars = {'path__startswith': dir_str}
            else:
                pars = {'path': dir_str}

            for o in FileMetadata.objects.filter(**pars):
                o.delete()
                c += 1
        return c

    def index_metadata_db(self, dirs_str=None, reindex=False):
        """
        Get the metadata from all directories (dirs_str) and save in the DB.

        :param reindex: delete all data and reindex
        :param dirs_str: list of directories. eg. ['/var/folder1','/var/folder2',]
        :return:
        """

        self.errors = []
        dirs_str = self.normalize_dirs(dirs_str)
        self.count_added = 0
        self.count_updated = 0
        self.count_deleted = 0

        if reindex:
            # FileMetadata.objects.all().delete;
            self.count_deleted = self.delete_metadata_db(dirs_str)

        for m in self.retrieve_metadata_files(dirs_str=dirs_str):
            try:
                if m:
                    try:
                        obj = FileMetadata.objects.get(path=m['path'], filename=m['filename'])
                        self.count_updated += 1
                    except FileMetadata.DoesNotExist:
                        self.count_added += 1
                        obj = FileMetadata()

                    # Set the field values
                    fields = [f.name for f in FileMetadata._meta.get_fields()]
                    for k, v in m.items():
                        if k in fields:
                            setattr(obj, k, v)
                    obj.save()
            except KeyboardInterrupt:
                raise
            except Exception as e:
                if self.raise_errors:
                    raise
                else:
                    self.errors.append("Error saving file %s - %s" % (m.get('filename', '[None]'), e))
