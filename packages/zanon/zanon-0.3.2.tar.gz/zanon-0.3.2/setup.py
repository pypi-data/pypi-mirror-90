import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zanon", 
    version="0.3.2",
    author="SmartData@PoliTO",
    author_email="s251325@studenti.polito.it",
    description="A module for z-anonymity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/pimcity/wp2/zeta-anonymity",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)