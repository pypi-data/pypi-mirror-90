import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="f-encrypt",
    version="1.01",
    license='',
    include_package_data=True,
    packages=["fencrypt"],
    install_requires=["Click", "pycryptodome"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Kyle Pericak',
    author_email='kyle@pericak.com',
    url="https://github.com/kylep/f-encrypt",
    download_url="https://github.com/kylep/f-encrypt/archive/1.01.tar.gz",
    classifiers=["Topic :: Security :: Cryptography"],
    entry_points={
        "console_scripts": [
            "f-encrypt = fencrypt.entrypoint:encrypt",
            "f-decrypt = fencrypt.entrypoint:decrypt",
        ]
    },
)
