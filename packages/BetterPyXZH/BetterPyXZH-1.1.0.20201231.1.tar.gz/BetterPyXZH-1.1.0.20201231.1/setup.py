# coding=utf-8
from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='BetterPyXZH',
    version='1.1.0.20201231.1',
    description=(
        'Use Something to Make Python Better!'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='OdorajBotoj',
    author_email='odoraj_botoj@tom.com',
    license='GNU General Public License',
    packages=find_packages(),
    url='https://github.com/OdorajBotoj/BetterPyXZH',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.5',
)
