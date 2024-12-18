import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OddEven-SP",
    version="1.0",
    author="Aarav Gupta",
    author_email="tribejustice35@gmail.com",
    description="So, welcome to my first ever Python Project! That is a game based on Odd Even, but with a twist of Cricket!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aarav2709/OddEven-SP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
