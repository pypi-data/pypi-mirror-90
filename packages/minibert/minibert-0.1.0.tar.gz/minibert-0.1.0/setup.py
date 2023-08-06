import setuptools

with open("README.md", "rt", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="minibert",
    version="0.1.0",
    author="Gaëtan Caillaut",
    author_email="gaetan.caillaut@univ-lemans.fr",
    description="A simplified implementation of BERT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git-lium.univ-lemans.fr/gcaillaut/minibert",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
