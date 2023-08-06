import setuptools
import upgrade_version

# f = open('VERSION.txt')
# version_str = f.read()
# f.close()
version_str = upgrade_version.get_version()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="siweilib",
    version=version_str,
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
