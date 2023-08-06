# -*- coding: utf-8 -*-

"""Console script for telegram-upload."""
import click

from telegram_upload.client import Client
from telegram_upload.config import default_config, CONFIG_FILE
from telegram_upload.exceptions import catch
from telegram_upload.files import NoDirectoriesFiles, RecursiveFiles, NoLargeFiles, SplitFiles

DIRECTORY_MODES = {
    'fail': NoDirectoriesFiles,
    'recursive': RecursiveFiles,
}
LARGE_FILE_MODES = {
    'fail': NoLargeFiles,
    'split': SplitFiles,
}


class MutuallyExclusiveOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help = kwargs.get('help', '')
        if self.mutually_exclusive:
            kwargs['help'] = help + (
                ' NOTE: This argument is mutually exclusive with'
                ' arguments: [{}].'.format(self.mutually_exclusive_text)
            )
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise click.UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(
                    self.name,
                    self.mutually_exclusive_text
                )
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(
            ctx,
            opts,
            args
        )

    @property
    def mutually_exclusive_text(self):
        return ', '.join([x.replace('_', '-') for x in self.mutually_exclusive])


@click.command()
@click.argument('files', nargs=-1)
@click.option('--to', default='me', help='Phone number, username, invite link or "me" (saved messages). '
                                         'By default "me".')
@click.option('--config', default=None, help='Configuration file to use. By default "{}".'.format(CONFIG_FILE))
@click.option('-d', '--delete-on-success', is_flag=True, help='Delete local file after successful upload.')
@click.option('--print-file-id', is_flag=True, help='Print the id of the uploaded file after the upload.')
@click.option('--force-file', is_flag=True, help='Force send as a file. The filename will be preserved '
                                                 'but the preview will not be available.')
@click.option('-f', '--forward', multiple=True, help='Forward the file to a chat (alias or id) or user (username, '
                                                     'mobile or id). This option can be used multiple times.')
@click.option('--directories', default='fail', type=click.Choice(list(DIRECTORY_MODES.keys())),
              help='Defines how to process directories. By default directories are not accepted and will raise an '
                   'error.')
@click.option('--large-files', default='fail', type=click.Choice(list(LARGE_FILE_MODES.keys())),
              help='Defines how to process large files unsupported for Telegram. By default large files are not '
                   'accepted and will raise an error.')
@click.option('--caption', type=str, help='Change file description. By default the file name.')
@click.option('--no-thumbnail', is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=["thumbnail_file"],
              help='Disable thumbnail generation. For some known file formats, Telegram may still generate a '
                   'thumbnail or show a preview.')
@click.option('--thumbnail-file', default=None, cls=MutuallyExclusiveOption, mutually_exclusive=["no_thumbnail"],
              help='Path to the preview file to use for the uploaded file.')
@click.option('-p', '--proxy', default=None,
              help='Use an http proxy, socks4, socks5 or mtproxy. For example socks5://user:pass@1.2.3.4:8080 '
                   'for socks5 and mtproxy://secret@1.2.3.4:443 for mtproxy.')
def upload(files, to, config, delete_on_success, print_file_id, force_file, forward, directories, large_files, caption,
           no_thumbnail, thumbnail_file, proxy):
    """Upload one or more files to Telegram using your personal account.
    The maximum file size is 2 GiB and by default they will be saved in
    your saved messages.
    """
    client = Client(config or default_config(), proxy=proxy)
    client.start()
    files = DIRECTORY_MODES[directories](files)
    if directories == 'fail':
        # Validate now
        files = list(files)
    files = LARGE_FILE_MODES[large_files](files)
    if large_files == 'fail':
        # Validate now
        files = list(files)
    if no_thumbnail:
        thumbnail = False
    elif thumbnail_file:
        thumbnail = thumbnail_file
    else:
        thumbnail = None
    client.send_files(to, files, delete_on_success, print_file_id, force_file, forward, caption, thumbnail)


@click.command()
@click.option('--from', '-f', 'from_', default='me',
              help='Phone number, username, chat id or "me" (saved messages). By default "me".')
@click.option('--config', default=None, help='Configuration file to use. By default "{}".'.format(CONFIG_FILE))
@click.option('-d', '--delete-on-success', is_flag=True,
              help='Delete telegram message after successful download. Useful for creating a download queue.')
@click.option('-p', '--proxy', default=None,
              help='Use an http proxy, socks4, socks5 or mtproxy. For example socks5://user:pass@1.2.3.4:8080 '
                   'for socks5 and mtproxy://secret@1.2.3.4:443 for mtproxy.')
def download(from_, config, delete_on_success, proxy):
    """Download all the latest messages that are files in a chatt, by default download
    from "saved messages". It is recommended to forward the files to download to
    "saved messages" and use parameter ``--delete-on-success``. Forwarded messages will
    be removed from the chat after downloading, such as a download queue.
    """
    client = Client(config or default_config(), proxy=proxy)
    client.start()
    messages = client.find_files(from_)
    client.download_files(from_, messages, delete_on_success)


upload_cli = catch(upload)
download_cli = catch(download)


if __name__ == '__main__':
    import sys
    import re
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    fn = {'upload': upload_cli, 'download': download_cli}[sys.argv[1]]
    sys.argv = [sys.argv[0]] + sys.argv[2:]
    sys.exit(fn())
