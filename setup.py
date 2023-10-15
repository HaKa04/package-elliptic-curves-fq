from setuptools import setup, find_packages

VERSION = '0.3.3'
DESCRIPTION = 'ECC Library'

with open("README.md", "r") as f:
    long_description = f.read()

long_description = long_description.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')


# Setting up
setup(
    name="elliptic_curves_fq", 
    version=VERSION,
    author="Kaspar Hui",
    author_email="<kaspar.hui@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    install_requires=[],
    keywords=['python', 'ECC', 'Finite Fields'],
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    url='https://github.com/HaKa04/package-elliptic-curves-fq'
)