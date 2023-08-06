import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='luchtmeetnet',
    version='0.0.2',
    author='Marcel Timmermans',
    author_email='marcel@timmermans.us',
    description="Package for luchtmeetned (Dutch)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/magtimmermans/python_luchtmeetnet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)