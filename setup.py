from setuptools import setup, find_packages
from mkbak import version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mkbak",
    version=version,
    author="Julia A M",
    author_email="jlearning@tuta.io",
    description="a commandline utility to create file backups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sudo-julia/mkbak",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
        "mkbak-iterfzf>=0.6.1",
        "rich>=9.8.2",
    ],
    python_requires=">=3.7",
    entry_points={"console_scripts": ["mkbak = mkbak.__main__:main"]},
)
