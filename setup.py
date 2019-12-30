import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="enconv",
    version="0.0.1",
    author="Joy Yeh",
    author_email="joyyeh.tw@gmail.com",
    description="Encodinger conversion wrapper around chardet.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joy13975/enconv",
    packages=setuptools.find_packages(),
    scripts=['bin/enconv'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=required,
)
