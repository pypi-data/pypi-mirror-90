from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tfwstartr",
    version="1.0.0",
    author="Avatao.com Innovative Learning Kft.",
    author_email="support@avatao.com",
    url="https://github.com/avatao-content/tfw-startr",
    license="Apache License 2.0",
    description="Bootstrap TFW tutorials for the Avatao platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["requests >= 2.25.1", "GitPython >= 3.1.11", "PyYaml >= 5.3.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    package_data={
        "": ["data/*.yaml"],
    },
)
