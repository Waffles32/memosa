
from setuptools import setup, find_packages

setup(
    name = "memosa",
    version = "0.4.0",
    author = "Forrest Button",
    author_email = "forrest.button@gmail.com",
    description = "",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/Waffles32/memosa",
    packages = find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	include_package_data = True,
	install_requires = open('requirements.txt').read().splitlines(),
	python_requires='>3.6',
	zip_safe = False,
)
