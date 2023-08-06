from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "pamona",
    version = "0.1.0",
    keywords = ("Pamona", "caokai", "amss"),
    description = "manifold alignment method for single-cell multi-omics integration using Pamona",
    python_requires=">=3.6",
    license = "MIT Licence",

    url = "https://github.com/caokai1073/Pamona",
    author = "caokai",
    author_email = "caokai@amss.ac.cn",

    packages = find_packages(),
    include_package_data = True,
    install_requires = [],
    platforms = "any",
)
