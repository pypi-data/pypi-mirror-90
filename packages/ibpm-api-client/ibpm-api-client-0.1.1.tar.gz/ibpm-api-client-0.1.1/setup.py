import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="ibpm-api-client",
    version="0.1.1",
    description="ibpm web api client",
    url="https://github.com/ibimec/ibpm-api-client",
    author="rgallini",
    author_email="riccardo.gallini@gmail.com",
    license="MIT",
    packages=["ibpm"],
    include_package_data=True,
    install_requires=["requests", "jsons", "pillow"],
)