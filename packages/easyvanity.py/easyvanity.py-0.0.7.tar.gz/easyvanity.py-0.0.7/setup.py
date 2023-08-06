from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name = 'easyvanity.py',
    version = '0.0.7',
    license = 'AGPL',
    author = 'Team Wezacon',
    author_email = 'wezacon.com@gmail.com',
    description = 'Easily create a vanity structure!',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    keywords = [
        'vanity',
        'bots-py',
        'wezacon'
    ],
    install_requires = [
        'setuptools',
        'requests',
        'six',
        'ujson',
        'pymongo',
        'dnspython'
    ],
    setup_requires = [
        'wheel'
    ],
    packages = find_packages()
)
