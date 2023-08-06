import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="us_census_api_extract",
    version="0.0.4",
    author="Anders Bergman",
    author_email="",
    description="Extract US census data (as a DataFrame) by inputting a list of demographic variables and US state codes.",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    url="https://github.com/AndoKalrisian/us_census_api_extract",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['progress-keeper','pandas','numpy'],
    license="MIT License"
)
