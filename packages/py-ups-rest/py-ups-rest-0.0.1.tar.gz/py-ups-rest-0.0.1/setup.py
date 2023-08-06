from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py-ups-rest",
    version="0.0.1",
    author="Sitolo",
    author_email="admin@sitolo.com",
    description="Python wrapper around UPS REST API's",
    long_description=long_description,
    url="https://github.com/sitolo/pyUPS",
    packages=find_packages(),
    python_requires='>=3.5'
)