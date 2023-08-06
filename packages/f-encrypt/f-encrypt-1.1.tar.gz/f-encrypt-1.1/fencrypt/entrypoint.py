""" Entrypoint for f-encrypt commands """
import click

import fencrypt.aes as aes
import fencrypt.lib as lib


@click.option("--keep/--rm", default=True, help="--rm to delete src file (F_ENCRYPT_RM overrides)")
@click.option("--output", "-o", default=None, help="Output path - default = <PATH>.ct")
@click.option("--key", "-k", envvar="F_ENCRYPT_KEY", default=None, help="Secret Key")
@click.argument("path")
@click.command()
def encrypt(path, key, output, keep):
    """ Encrypt the given file """
    lib.echo(f"Encrypting - source file: {path}", 2)
    lib.validate_path(path, encrypt=True)
    output = lib.get_output(path, output)
    key = lib.get_key(key)
    with open(path, "rb") as fil:
        lib.echo(f"Reading {path}", 2)
        plaintext = fil.read()
    ciphertext = aes.encrypt(key, plaintext)
    with open(output, "w") as fil:
        lib.echo(f"Writing {output}", 2)
        fil.write(ciphertext)
    lib.delete_file(path, keep)


@click.option("--keep/--rm", default=True, help="--rm to delete src file (F_ENCRYPT_RM overrides)")
@click.option("--output", "-o", default=None, help="Output path - default = <PATH> (without .ct)")
@click.option("--key", "-k", envvar="F_ENCRYPT_KEY", default=None, help="Secret Key")
@click.argument("path")
@click.command()
def decrypt(path, key, output, keep):
    """ Dycrypt a given file """
    lib.echo(f"Decrypting - source file: {path}", 2)
    lib.validate_path(path, encrypt=False)
    output = lib.get_output(path, output)
    key = lib.get_key(key)
    with open(path, "r") as fil:
        lib.echo(f"Reading {path}", 2)
        ciphertext = fil.read()
    plaintext = aes.decrypt(key, ciphertext)
    with open(output, "wb") as fil:
        lib.echo(f"Writing {output}", 2)
        fil.write(plaintext)
    lib.delete_file(path, keep)
