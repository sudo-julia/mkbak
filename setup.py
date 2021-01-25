# pylint: disable=missing-module-docstring
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sudo-julia",
    version="0.7.1",
    author="Julia A M",
    author_email="jlearning@tuta.io",
    description="a commandline utility to create file backups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sudo-julia/mkbak",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: Terminals",
    ],
    install_requires=[
        "iterfzf>=0.5.0",
        "rich>=9.8.2",
    ],
    python_requires=">=3.7",
)
