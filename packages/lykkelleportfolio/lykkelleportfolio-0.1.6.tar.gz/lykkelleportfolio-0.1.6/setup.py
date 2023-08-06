import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lykkelleportfolio", # Replace with your own username
    version="0.1.6",
    author="Lykkelle Inc",
    author_email="admin@lykkelle.com",
    description="Modules pertaining to calculating portfolio data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dev.azure.com/lykkelle/Lykkelle/_git/Lykkellescripts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)