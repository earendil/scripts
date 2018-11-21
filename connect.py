import sh
import click

TMP_MOUNT_POINT = '/tmp/test'


class RemoteMount(object):

    def __init__(self, server, repo):
        self.server = server
        self.repo = repo

    def __enter__(self):
        return self

    def __exit__(self, *args):
        sh.fusermount3('-u', TMP_MOUNT_POINT)

    def mount(self):
        sh.sshfs('{}:{}'.format(self.server, self.repo), TMP_MOUNT_POINT)


@click.command()
@click.argument('server')
@click.option("--repo", default="test", help="Which repo to mount.")
def main(server, repo):
    """
    server:        A box to connect to.
    """
    with RemoteMount(server, repo) as r:
        print "Mounting {}'s {} repo at {}".format(server, repo, TMP_MOUNT_POINT)
        r.mount()
        raw_input("Press any key to exit and unmount...")


if __name__ == '__main__':
    main()

# TODO: Handle potential exceptions thrown by sshfs and fusermount
# TODO: Find a better way to wait/halt execution
