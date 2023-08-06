import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="esbulkjsonconvertnormaljson",
    version="0.0.1",
    author="Jayakrishna narra",
    author_email="jknarra8@gmail.com",
    description="A bulk es json file to normal json file",
    long_description=long_description + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    License='MIT',
    keywords='elasticsearch',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
