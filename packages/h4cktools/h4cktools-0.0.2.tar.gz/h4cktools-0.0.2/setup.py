from setuptools import setup, find_packages


setup(
    name="h4cktools",
    version="0.0.2",
    description="h4cktools is a python library containing usefull helpers "
    "for penetration testing and security challenges.",
    url="https://github.com/WhatTheSlime/h4cktools",
    author="Sélim Lanouar",
    author_email="selim.lanouar@gmail.com",
    license="CeCILL",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "urllib3==1.25.9",
        "requests_mock==1.8.0",
        "lxml==4.5.2",
        "requests==2.23.0",
        "beautifulsoup4==4.9.3"
    ],
    extras_require={
        "tests": [
            "pytest==6.1.2",
            "pytest-asyncio",
            "pytest-cov"
        ],
    }
)
