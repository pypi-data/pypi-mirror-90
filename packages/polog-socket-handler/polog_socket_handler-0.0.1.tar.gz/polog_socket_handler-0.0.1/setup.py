from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ['python-dateutil==2.8.1']

setup(
    name="polog_socket_handler",
    version="0.0.1",
    author="Fedor Malkov",
    author_email="qwert199600@mail.ru",
    description="Handler для polog",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Thereodorex/polog_handler_socket",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)