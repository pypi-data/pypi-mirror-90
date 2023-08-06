from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name = 'easyDefine.py',
    version = '0.0.2',
    license = 'MIT',
    author = 'Team Wezacon',
    author_email = 'wezacon.com@gmail.com',
    description = 'The easiest functions for your app.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    keywords = [
        'easyDefine',
        'easyDefine-py',
        'wezacon'
    ],
    install_requires = [
        'setuptools',
        'requests',
        'six',
        'ujson'
    ],
    setup_requires = [
        'wheel'
    ],
    packages = find_packages()
)
