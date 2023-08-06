import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-utils-forsythetony", # Replace with your own username
    version="0.0.5",
    author="Anthony Forsythe",
    author_email="forsythetony+python@gmail.com",
    description="A package of common utilities (vague I know...)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/forsythetony/python-utilities",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)