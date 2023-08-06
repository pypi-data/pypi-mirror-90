from setuptools import setup, find_packages


with open('VERSION', 'r+') as file:
    version = file.read()

setup(
    name='Hubot',
    version=version,
    author="Clément Kérébel",
    author_email="clement.kerebel@coddity.com",
    url="https://gitlab.com/coddity/hubot/hubot_back",
    py_modules=['lib_back_hubot'],
    install_requires=['pandas'],
    extras_require={
        'test': ['pytest', 'flake8'],
        'deployment': ['twine']
    },
    packages=find_packages(exclude=('test',))
)
