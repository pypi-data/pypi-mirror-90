import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pheidi", # Replace with your own username
    version="0.0.12",
    author="Austin",
    author_email="",
    description="High speed ring buffer messaging system using shared memory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aschi2/pheidi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['msgpack','msgpack_numpy'],
    python_requires='>=3.8',
)
