from django.core.management.base import BaseCommand

from filemetadata.indexer import FileIndexer


class Command(BaseCommand):
    help = 'Update the the file-metadata found in the directories into the DB.'

    def add_arguments(self, parser):
        parser.add_argument('-f', dest='folders', type=str, required=False,
                            help="Folder(s) to index (coma separated)")
        parser.add_argument('-c', dest='clear', default=False, action='store_true',
                            help="Clear the data before reindex")
        parser.add_argument('-d', dest='delete', default=False, action='store_true',
                            help="Delete only the data from these folders and exit")
        parser.add_argument('-s', dest='symlinks', default=False, action='store_true',
                            help="Index the symlinks (Do not follow it)")
        parser.add_argument('-x', dest='content', default=False, action='store_true',
                            help="Extract the content of the file (text)")
        parser.add_argument('-n', dest='non_reentrant', default=False, action='store_true',
                            help="Non-reentrant mode (Not recursive)")
        parser.add_argument('-a', dest='abort', default=False, action='store_true',
                            help="Abort on errors")

    def handle(self, *args, **options):
        folders_str = None
        if options.get('folders', None):
            # TODO: find a better solution to allow ',' in the name of the folder
            folders_str = options['folders'].split(",")
        file_indexer = FileIndexer(follow_symlinks=not options.get('symlinks', False),
                                   extract_content=options.get('content', False),
                                   recursive=not options.get('non_reentrant', False),
                                   raise_errors=options.get('abort', False),
                                   verbose_print=True)
        if options.get('delete', False):
            file_indexer.count_deleted = file_indexer.delete_metadata_db(dirs_str=folders_str)
        else:
            file_indexer.index_metadata_db(dirs_str=folders_str,
                                           reindex=options.get('clear', False))

        if file_indexer.errors:
            msg = "Process executed with %s errors!" % len(file_indexer.errors)
        else:
            msg = "Process successful!"

        print("%s (deleted: %s, added: %s, updated: %s)\n%s" % (
            msg,
            file_indexer.count_deleted,
            file_indexer.count_added,
            file_indexer.count_updated,
            '\n'.join(file_indexer.errors)))
