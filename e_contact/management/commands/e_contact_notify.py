import djclick as click

from e_contact.utils import notify


@click.command()
def command():
    notified = notify()
    print('Notified? {}'.format(notified))
