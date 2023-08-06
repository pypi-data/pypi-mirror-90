import os
import re

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

init_py = os.path.join(os.path.dirname(__file__), "travitia_talk", "__init__.py")

with open(init_py) as f:
    cont = f.read()

    str_regex = r"['\"]([^'\"]*)['\"]"
    try:
        version = re.findall(rf"^__version__ = {str_regex}$", cont, re.MULTILINE)[0]
    except IndexError:
        raise RuntimeError(f"Unable to find version in {init_py}")

    try:
        author = re.findall(rf"^__author__ = {str_regex}$", cont, re.MULTILINE)[0]
    except IndexError:
        raise RuntimeError(f"Unable to find author in {init_py}")

install_requires = ["aiohttp"]

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Typing :: Typed",
]

setuptools.setup(
    name="travitia_talk",
    version=version,
    author=author,
    author_email="fogaprod@gmail.com",
    description="ChatBot API wrapper for https://public-api.travitia.xyz/talk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fogapod/travitia-talk",
    install_requires=install_requires,
    python_requires=">=3.6",
    packages=setuptools.find_packages(),
    package_data={"travitia_talk": ["py.typed"]},
    license="MIT",
    classifiers=classifiers,
)
