from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: MacOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'SLC',
    version = '0.3.2b2',
    description = 'A tool that allows you to connect to and run SQL commands to an SQLite3 database easily.',
    long_description_content_type = 'text/markdown',
    long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    url = 'https://downloadSLC.jonathan2018.repl.co/dev/pr/downloads/SLC-0.3.2b2.tar.gz',
    author = 'Jonathan Wang',
    author_email = 'jonathanwang2018@gmail.com',
    License = 'MIT',
    classifiers = classifiers,
    keywords = 'SQL, SQLite3, Database',
    packages = find_packages(),
    install_requires=['sqlite3']
)
