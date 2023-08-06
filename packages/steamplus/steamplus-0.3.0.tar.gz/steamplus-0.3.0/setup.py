from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="steamplus",
    packages=find_packages(include=["steamplus"]),
    version="0.3.0",
    license="GPL-3.0-only",
    description="A library for extracting data from steam via steam storefront api and steamspy api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Team Ster",
    author_email="martijn.business@hotmail.com",
    url="https://github.com/MartijnCBV/steamplus/wiki",
    download_url="https://github.com/MartijnCBV/steamplus/archive/0.3.0.tar.gz",
    keywords=["steam", "statistics", "valve"],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Topic :: Games/Entertainment"
    ],
    python_requires=">=3.8",
    setup_requires=["pytest-runner"],
    tests_require=["pytest===6.2.1"],
    test_suite="tests"
)
