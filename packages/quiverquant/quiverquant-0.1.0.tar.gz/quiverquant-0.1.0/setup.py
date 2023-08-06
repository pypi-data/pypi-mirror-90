import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quiverquant",
    version="0.1.0",
    author="Chris Kardatzke",
    author_email="chris@quiverquant.com",
    description="Package for Quiver Quantitative Alternative Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Quiver-Quantitative/python-api",
    py_modules = ["quiverquant"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)