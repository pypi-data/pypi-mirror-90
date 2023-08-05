import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="siweilib",
    version="0.0.2.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=("tests",)),
    python_requires='>=3.5',
    install_requires=[
        "termcolor",
        "pytz",
        "argparse",
        "cryptography",
    ]
)
