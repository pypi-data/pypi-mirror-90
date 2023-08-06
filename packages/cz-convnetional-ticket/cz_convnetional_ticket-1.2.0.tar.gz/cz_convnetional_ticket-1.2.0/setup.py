from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cz_convnetional_ticket",
    version="1.2.0",
    py_modules=["cz_convnetional_ticket"],
    license="MIT",
    description= "Conventional commits with tickets in changelog",
    author="Gohar Anwar",
    author_email="gohar@goharanwar.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["commitizen"],
)
