import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kiwiml",
    version="0.0.3",
    author="Ori Yonay",
    author_email="oriyonay12@gmail.com",
    description="a tiny, simple, instructional machine learning library in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oriyonay/kiwiml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
