import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-nba-stats",
    version="0.0.3",
    author="Kelvin Hu",
    author_email="kelvin.hu.1203@gmail.com",
    description="A package for scraping NBA stats from yahoo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/monootc/nba_stats",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
