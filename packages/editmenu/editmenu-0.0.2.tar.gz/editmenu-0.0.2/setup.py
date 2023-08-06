import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="editmenu", 
    version="0.0.2",
    author="Aswin Rajasekharan",
    author_email="aswin4400@gmail.com",
    description="A simple multiline edit menu for CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aswin4400/editmenu.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)