"""Console script for docs2txt."""
import sys
import click

from docs2txt.utils import create_save_directory


@click.command()
@click.option('-u', '--url', prompt='URL', help='The URL to process.')
@click.option('-o', '--output-dir', prompt='Output Dir', default='~/docs2txt/',
              help='The path where the output will be saved.')
def docs_rs(url, output_dir):
    from docs2txt.docs_rs import main
    """Process a URL and save the output at a given path."""
    # Replace this with your actual processing and saving code.
    click.echo(f'Processing URL: {url}')
    output_dir = create_save_directory(output_dir)
    click.echo(f'Saving at: {output_dir}')
    save_path = main(url, output_dir)
    click.echo(f'Output saved at: {save_path}')


@click.group()
def cli():
    pass


cli.add_command(docs_rs)

if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
