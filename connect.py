import sh
import click

TMP_PATH = '/tmp/remote'
sh.mkdir('-p', TMP_PATH)


def ensure_safe(f):
    def inner(*args):
        try:
            sh.fuser('-k', TMP_PATH)
            sh.fusermount3('-u', TMP_PATH)
        except sh.ErrorReturnCode_1:
            f(*args)
    return inner


class RemoteMount(object):

    def __init__(self, server, repo):
        self.server = server
        self.repo = repo

    def __enter__(self):
        return self

    @ensure_safe
    def __exit__(self, *args):
        pass

    @ensure_safe
    def mount(self):
        sh.sshfs('{}:{}'.format(self.server, self.repo), TMP_PATH)


@click.command()
@click.argument('server')
@click.option("--repo", default="test", help="Which repo to mount.")
def main(server, repo):
    """
    server:        A box to connect to.
    """
    with RemoteMount(server, repo) as r:
        print "Mounting {}'s {} repo at {}".format(server, repo, TMP_PATH)
        r.mount()
        raw_input("Press any key to exit and attempt to unmount...")


if __name__ == '__main__':
    main()
