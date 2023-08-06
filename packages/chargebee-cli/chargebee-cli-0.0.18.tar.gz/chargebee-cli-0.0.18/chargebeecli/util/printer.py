import click


def custom_print(message):
    click.echo(message)


def custom_print_error(message):
    click.echo(message, err=True)
