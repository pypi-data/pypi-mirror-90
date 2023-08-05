import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wordsapy",
    version="1.1.1",
    author="Sergio Contreras Agustí (backrndsource)",
    author_email="backrndsource@gmail.com",
    description="Wordsapy is a python integration for the WordsAPI, that allows developers to retrieve information about English words like a dictionary.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/backrndsource/wordsapy",
    packages=setuptools.find_packages(),
    keywords=["words", "dictionary" "wordsapi", "api", "wrapper", "interface", "client", "database"],
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
