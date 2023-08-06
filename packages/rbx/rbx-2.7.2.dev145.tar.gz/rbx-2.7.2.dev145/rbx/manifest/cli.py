import click

from .processor import ManifestHandler, zip_images
from ..settings import AWS_BUCKET


@click.command(help='Get the manifest from a url.')
@click.argument('url')
@click.option('-f', '--filename', default='out',
              help='Name of Zip File to output.')
@click.option('-b', '--bucket', default=AWS_BUCKET,
              help='Optional bucket path')
def build_image_from_manifest(url, filename, bucket):
    handler = ManifestHandler()

    image_list = handler.build_image_from_manifest(manifest=url, bucket=bucket)
    click.echo("Image Generated!")

    zip_images(image_list, filename=filename)
    click.echo("Image Now Available in {}.zip".format(filename))
