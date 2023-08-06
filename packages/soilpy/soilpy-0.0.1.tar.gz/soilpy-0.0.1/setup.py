import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="soilpy",
    version="0.0.1",
    author="Nick Machairas",
    author_email="nick@groundwork.ai",
    description="General Purpose Soil Mechanics Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/groundworkai/soilpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
