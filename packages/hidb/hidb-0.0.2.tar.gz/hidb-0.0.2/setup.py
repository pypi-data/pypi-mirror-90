import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hidb",
    version="0.0.2",
    author="Sudhanshu Kumar",
    author_email="sudhanshukumar5459@gmail.com",
    description="It is a file based key value data store ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sk-ip/hidb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
