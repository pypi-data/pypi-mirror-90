import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy_template",
    version="0.0.1",
    author="Balthasar Hofer",
    author_email="lebalz@outlook.com",
    description="Create and process templates with ease",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lebalz/easy_template",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
