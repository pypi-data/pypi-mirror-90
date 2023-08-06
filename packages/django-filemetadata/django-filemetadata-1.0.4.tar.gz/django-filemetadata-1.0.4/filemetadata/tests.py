import os

from django.test import TestCase

from filemetadata.indexer import FileIndexer
from filemetadata.models import FileMetadata


def sort(data):
    data.sort()
    return data


class StaticFileTest(TestCase):

    def test_retrieve_metadata_files(self):
        test_folder_a = os.path.join("filemetadata", "tests", "folder_A")
        test_folder_c = os.path.join("filemetadata", "tests", "folder_C")

        file_indexer = FileIndexer(extract_content=True, recursive=True, raise_errors=False)
        res = file_indexer.retrieve_metadata_files(dirs_str=test_folder_a)
        self.assertEqual(len(file_indexer.errors), 0)
        self.assertEqual(len(res), 3)

        # Prepare the results for tests
        fields2test = ['filename', 'size', 'size_str', 'title', 'text_content']
        res_test = {}
        for r in res:
            res_test[r['filename']] = r

        self.assertEqual(
            [(k, v) for k, v in res_test['test_file3.txt'].items() if k in fields2test],
            [('filename', 'test_file3.txt'),
             ('size', 30),
             ('size_str', '30.00 bytes'),
             ('title', 'test_file3.txt'),
             ('text_content', b"This is\nMy Test 3.\nThat's all!")]
        )

        self.assertEqual(
            [(k, v) for k, v in res_test['test_file1.txt'].items() if k in fields2test],
            [('filename', 'test_file1.txt'),
             ('size', 26),
             ('size_str', '26.00 bytes'),
             ('title', 'test_file1.txt'),
             ('text_content', b'This is\nMy Test 1.\nThanks!')]

        )

        self.assertEqual(
            [(k, v) for k, v in res_test['test_file2.txt'].items() if k in fields2test],
            [('filename', 'test_file2.txt'),
             ('size', 27),
             ('size_str', '27.00 bytes'),
             ('title', 'test_file2.txt'),
             ('text_content', b'This is\nMy Test 2.\nSee You!')]
        )

        file_indexer = FileIndexer(extract_content=False)
        res = file_indexer.retrieve_metadata_files(dirs_str=test_folder_c)
        self.assertEqual(
            [(k, v) for k, v in res[0].items() if k in ['filename', 'size', 'size_str', 'title', 'text_content']],
            [('filename', 'test_file4.txt'),
             ('size', 24),
             ('size_str', '24.00 bytes'),
             ('title', 'test_file4.txt'),
             ('text_content', '')]
        )

    def test_index_metadata_db(self):
        """
        Testing sync a file.
        :return:
        """

        test_folder_a = os.path.join("filemetadata", "tests", "folder_A")
        test_folder_c = os.path.join("filemetadata", "tests", "folder_C")

        file_indexer = FileIndexer(extract_content=True, recursive=True, raise_errors=False)
        file_indexer.index_metadata_db(dirs_str=test_folder_a, reindex=False)
        self.assertEqual(file_indexer.count_added, 3)
        self.assertEqual(file_indexer.count_deleted, 0)
        self.assertEqual(file_indexer.count_updated, 0)
        self.assertEqual(len(file_indexer.errors), 0)
        self.assertEqual(sort([o.filename for o in FileMetadata.objects.all()]),
                         ['test_file1.txt', 'test_file2.txt', 'test_file3.txt'])

        # Test reindex
        file_indexer.index_metadata_db(dirs_str=test_folder_a, reindex=True)
        self.assertEqual(file_indexer.count_added, 3)
        self.assertEqual(file_indexer.count_deleted, 3)
        self.assertEqual(file_indexer.count_updated, 0)
        self.assertEqual(len(file_indexer.errors), 0)
        self.assertEqual(sort([o.filename for o in FileMetadata.objects.all()]),
                         ['test_file1.txt', 'test_file2.txt', 'test_file3.txt'])

        # Test multiple folders
        file_indexer.index_metadata_db(dirs_str=[test_folder_a, test_folder_c], reindex=False)
        self.assertEqual(file_indexer.count_added, 1)
        self.assertEqual(file_indexer.count_deleted, 0)
        self.assertEqual(file_indexer.count_updated, 3)
        self.assertEqual(len(file_indexer.errors), 0)
        self.assertEqual(sort([o.filename for o in FileMetadata.objects.all()]),
                         ['test_file1.txt', 'test_file2.txt', 'test_file3.txt', 'test_file4.txt'])

        # Test delete (non recursive)
        file_indexer = FileIndexer(recursive=False)
        deleted = file_indexer.delete_metadata_db(dirs_str=test_folder_a)
        self.assertEqual(deleted, 2)
        self.assertEqual(sort([o.filename for o in FileMetadata.objects.all()]),
                         ['test_file3.txt', 'test_file4.txt'])

        # Test delete (recursive)
        file_indexer = FileIndexer(recursive=True)
        deleted = file_indexer.delete_metadata_db([test_folder_a, test_folder_c])
        self.assertEqual(deleted, 2)
        self.assertEqual(sort([o.filename for o in FileMetadata.objects.all()]),
                         [])

    def test_index_metadata_db_options(self):
        test_folder_a = os.path.join("filemetadata", "tests", "folder_A")
        test_file1 = os.path.join("filemetadata", "tests", "folder_A", "test_file1.txt")

        # Test non-recursive
        file_indexer = FileIndexer(recursive=False)
        file_indexer.index_metadata_db(dirs_str=test_folder_a)
        self.assertEqual(file_indexer.count_added, 2)
        self.assertEqual(sort([o.filename for o in FileMetadata.objects.all()]),
                         ['test_file1.txt', 'test_file2.txt'])

        # Test raise_errors
        file_indexer.raise_errors = True
        self.assertRaises(FileNotFoundError, file_indexer.index_metadata_db, dirs_str=[test_file1,
                                                                                       test_folder_a,
                                                                                       'wrong_folder_error'])

        # Test raise_errors
        file_indexer.raise_errors = False
        file_indexer.index_metadata_db(dirs_str=[test_file1,
                                                 test_folder_a,
                                                 'wrong_folder_error'])
        self.assertEqual(len(file_indexer.errors), 2)
