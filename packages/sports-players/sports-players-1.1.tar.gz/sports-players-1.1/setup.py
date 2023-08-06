from setuptools import setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sports-players",
    version="1.1",
    description="Sports Players Objects",
    packages=["sports_players"],
    install_requires=[
        "pandas",
    ],
    author="Frantz Paul",
    author_email="fpaul787@gmail.com",
    zip_safe=False,
    long_description=long_description,
    long_description_content_type="text/x-rst",
)
