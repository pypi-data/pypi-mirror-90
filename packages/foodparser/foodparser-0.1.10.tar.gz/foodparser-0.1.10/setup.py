from setuptools import setup, find_packages
import pkg_resources
# from foodparser import foodparser

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

# requirements = ["ipython>=6", "nbformat>=4", "nbconvert>=5", "requests>=2"]

setup(
    name="foodparser",
    version='0.1.10',
    author="Joey Hou",
    author_email="z9hou@ucsd.edu",
    description="A package to parse food logging texts.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/JoeyHou/food_parser",
    packages=find_packages(),
    # install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    package_data = {
        "foodparser": ["data/combined_gram_set.csv"]
    }
)
