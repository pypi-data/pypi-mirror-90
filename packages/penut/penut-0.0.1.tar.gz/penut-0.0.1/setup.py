import setuptools

setuptools.setup(
    name="penut",
    version="0.0.1",
    author="PenutChen",
    author_email="penut85420@gmail.com",
    description="This is a collection of my useful functions.",
    long_description=open('README.md', 'r', encoding='UTF-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/penut85420/Penut",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
