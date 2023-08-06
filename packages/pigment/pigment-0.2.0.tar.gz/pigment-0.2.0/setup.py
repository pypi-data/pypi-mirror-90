from pathlib import Path

import setuptools

long_description = (Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    name="pigment",
    version="0.2.0",
    author="Ben Soyka",
    author_email="bensoyka@icloud.com",
    description="Python utilities for colors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bsoyka/pigment",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    project_urls={
        "Documentation": "https://pigment.readthedocs.io/",
        "Changelog": "https://github.com/bsoyka/pigment/releases",
    },
)
