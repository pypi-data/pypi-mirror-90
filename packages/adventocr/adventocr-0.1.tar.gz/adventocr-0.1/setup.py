from setuptools import setup, find_packages

setup(
    name="adventocr",
    version="0.1",
    description="Parsing text output for Advent of Code puzzles",
    url="https://github.com/cqkh42/aoc_letters",
    author="cqkh42",
    author_email="jackcooper93@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    install_requires=[
    ],
    packages=find_packages()
)
