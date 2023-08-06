import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name ="MenuBuilder",
    version="1.2",
    author = "Ewen",
    author_email = "1lorimerewe2@gmail.com",
    description = "A simple commandline menu builder",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/OOgaboogaboog/MenuBuilder",
    packages= setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",

        
        "Operating System :: OS Independent"

    ],
    python_requires='<=3.9',
)

