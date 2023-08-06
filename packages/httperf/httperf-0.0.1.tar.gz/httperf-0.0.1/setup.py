import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="httperf", # Replace with your own username
    version="0.0.1",
    author="Luke Hartman",
    author_email="ljhartman10@gmail.com",
    license="MIT",
    description="A lightweight python API testing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luhart/perf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
