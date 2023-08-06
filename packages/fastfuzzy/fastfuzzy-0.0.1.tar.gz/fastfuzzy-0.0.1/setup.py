#!/usr/bin/env python

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="fastfuzzy",
    version="0.0.1",
    author="Carsten Schnober",
    author_email="carschno@gmail.com",
    description="Fast fuzzy string matching.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/carschno/fastfuzzy",
    packages=setuptools.find_packages(where="src"),
    package_dir={"fastfuzzy": "src/fastfuzzy"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7,<3.9",
    install_requires=["abydos==0.5.0", "tqdm==4.55.1"],
    extras_require={"test": ["pytest==6.2.1", "pytest-cov==2.10.1"]},
)
