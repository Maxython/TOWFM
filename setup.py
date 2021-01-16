import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="TOWFM",
    version="0.1",
    author="Maxython",
    description="Create any tree format",
    long_description=long_description,
    url="https://github.com/Maxython/TOWFM",
    license="MIT",
    packages=setuptools.find_packages(),
)
