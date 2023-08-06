from setuptools import setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

    setup(
        name="simplevault",
        version="3.9",
        url="https://gitlab.com/traxix/python/simplevault",
        packages=[".", "simplevault"],
        scripts=["simplevault/simplevault-cli"],
        install_requires=required,
        license="GPLv3",
        author="trax Omar Givernaud",
    )
