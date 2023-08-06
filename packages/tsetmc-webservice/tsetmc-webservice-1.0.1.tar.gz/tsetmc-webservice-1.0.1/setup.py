from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    # region core
    name="tsetmc-webservice",
    version="1.0.1",
    python_requires=">=3.5",
    install_requires=[
        "pandas",
        "zeep",
    ],
    extras_require={
        "dev": []
    },
    dependency_links=[],
    packages=find_packages(exclude=["scripts"]),
    # endregion
    # region data & scripts
    # endregion
    # region metadata
    description="api to communicate with tsetmc webservice (the paid one)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mahs4d/tsetmc-webservice/",
    author="Mahdi Sadeghi",
    author_email="mail2mahsad@gmail.com",
    classifiers=[  # https://pypi.org/classifiers/
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="sample setuptools development",
    project_urls={
        "Bug Reports": "https://github.com/mahs4d/tsetmc-webservice/issues",
        "Source": "https://github.com/mahs4d/tsetmc-webservice/",
    },
    # endregion
)
