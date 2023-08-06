import setuptools

with open("README.md") as file:
    long_description = file.read()

setuptools.setup(
    name="pigment",
    version="0.3.0",
    author="Ben Soyka",
    author_email="bensoyka@icloud.com",
    description="Python utilities for colors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pigment.readthedocs.io/",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    project_urls={
        "Source": "https://github.com/bsoyka/pigment",
        "Changelog": "https://github.com/bsoyka/pigment/releases",
    },
    install_requires=["averager==2.0.0"],
)
