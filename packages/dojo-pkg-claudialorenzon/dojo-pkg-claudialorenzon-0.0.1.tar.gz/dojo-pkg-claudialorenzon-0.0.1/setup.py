import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dojo-pkg-claudialorenzon", # Replace with your own username
    version="0.0.1",
    author="Claudia Lorenzon",
    author_email="claudialorenzon@yahoo.it",
    description="Un piccolo package per il corso di Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/claudialorenzon/python3_dojo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)