import sh
import click

TMP_PATH = '/tmp/remote'


def ensure_safe(f):
    def inner(*args):
        try:
            sh.fuser('-k', TMP_PATH)
        except sh.ErrorReturnCode_1 as e:
            print e
        try:
            sh.fusermount('-u', TMP_PATH)
        except sh.ErrorReturnCode_1 as e:
            print e

        f(*args)
    return inner


class RemoteMount(object):

    def __init__(self, server, repo):
        self.server = server
        self.repo = repo

    def __enter__(self):
        sh.mkdir('-p', TMP_PATH)
        self.mount()

    @ensure_safe
    def __exit__(self, *args):
        pass

    @ensure_safe
    def mount(self):
        print "Mounting {}'s {} repo at {}".format(self.server, self.repo, TMP_PATH)
        sh.sshfs('{}:{}'.format(self.server, self.repo), TMP_PATH)


@click.command()
@click.argument('server')
@click.option("--repo", default="test", help="Which repo to mount.")
def main(server, repo):
    """
    server:        A box to connect to.
    """
    with RemoteMount(server, repo):
        raw_input("Press any key to exit and attempt to unmount...")


if __name__ == '__main__':
    main()
