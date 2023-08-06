import setuptools

with open('README.rst') as file:
    readme = file.read()

name = 'ldbcache'

version = '0.0.0'

author = 'Exahilosys'

url = f'https://github.com/{author}/{name}'

setuptools.setup(
    name = name,
    version = version,
    author = author,
    url = url,
    py_modules = [
        name
    ],
    license = 'MIT',
    description = 'Local dabatase caching.',
    long_description = readme,
    install_requires = [
        'pathing'
    ]
)
