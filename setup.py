import pathlib
from setuptools import setup

# Dynamically read the README file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="OddEven-SP",
    version="1.3.0",
    packages=["OddEvenSP"],
    description="So, welcome to my first ever Python Project! That is a game based on Odd Even, but with a twist of Cricket!",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Aarav Gupta",
    author_email="tribejustice35@gmail.com",
    url="https://github.com/Aarav2709/OddEven-SP",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games",
    ],
    python_requires=">=3.11",
    keywords="OddEven, SinglePlayer, Game, Cricket, Python",
    license="Apache Software License",
)
