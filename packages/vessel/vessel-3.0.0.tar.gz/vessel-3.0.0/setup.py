import setuptools

with open('README.rst') as file:
    readme = file.read()

name = 'vessel'

version = '3.0.0'

author = 'Exahilosys'

url = f'https://github.com/{author}/{name}'

setuptools.setup(
    name = name,
    version = version,
    author = author,
    url = url,
    packages = setuptools.find_packages(),
    license = 'MIT',
    description = 'Dynamic data access.',
    long_description = readme,
    extras_require = {
        'docs': [
            'sphinx'
        ]
    }
)
