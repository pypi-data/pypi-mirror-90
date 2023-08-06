import setuptools
from pydotmap._version import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydotmap",
    version=__version__,
    author="Atul Singh",
    author_email="atulsingh0401@gmail.com",
    description="Dot notation python dicationary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iamatulsingh/pydotmap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
