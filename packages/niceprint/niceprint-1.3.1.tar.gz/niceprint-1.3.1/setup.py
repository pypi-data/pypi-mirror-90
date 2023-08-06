from setuptools import setup

setup(
    name="niceprint",
    version='1.3.1',
    author="AstralDev",
    author_email="ekureedem480@gmail.com",
    description="A simple module for print.",
    long_description_content_type="text/markdown",
    long_description=str(open("README.md").read()),
    license="MIT",
    py_modules=["niceprint"],
    install_requires=["color"],
)
