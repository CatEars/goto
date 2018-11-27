'''Command Line Interface for working with Goto.
'''
import click

@click.command()
@click.option('--add', help='')
def main():
    '''Helper for jumpting to anywhere on your computer!'''
    click.echo('Hello World!')
