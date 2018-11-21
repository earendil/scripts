import sh
from os import path
import click

HOME = path.expanduser('~/')
SCIVISUM = HOME + 'workspace/scivisum'
CVS = HOME + 'cvs'
TMP_MOUNT_POINT = '/tmp/repo'


class RemoteMount(object):

    def __init__(self, server, repo):
        self.server = server
        self.repo = repo

    def __enter__(self):
        return self

    def __exit__(self):
        if self.path:
            sh.umount(TMP_MOUNT_POINT)

    @property
    def path(self):
        if self.repo == 'scivisum':
            return SCIVISUM
        elif self.repo == 'cvs':
            return CVS

    def mount(self):
        if self.path:
            sshfs = sh.sshfs.bake('-o', 'allow_other')
            sshfs('{}:{}'.format(self.server, self.path), '/tmp/repo')


@click.command()
@click.argument('server', help='A box to connect to.')
@click.option("-r", "--repo", default="scivisum", help="Which repo to mount.")
def main(server, repo):
    with RemoteMount(server, repo) as r:
        print "Mounting {}'s {} repo at {}".format(server, repo, TMP_MOUNT_POINT)
        r.mount()
        raw_input("Press any key to exit and unmount...")

# TODO: Handle potential exceptions thrown by sshfs and umount
# TODO: Find a better way to wait/halt execution
