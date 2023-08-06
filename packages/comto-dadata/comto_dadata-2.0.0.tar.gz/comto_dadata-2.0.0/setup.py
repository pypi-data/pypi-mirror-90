import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="comto_dadata",
    version="2.0.0",
    author="Pavel Vasin",
    author_email="commercito@gmail.com",
    description="Package for working with the \"dadata.ru\" service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://commercito.ru",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
