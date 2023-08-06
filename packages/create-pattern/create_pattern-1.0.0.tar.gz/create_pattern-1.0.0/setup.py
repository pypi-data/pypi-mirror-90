import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="create_pattern", # Replace with your own username
    version="1.0.0",
    author="Akshat Tiwari",
    author_email="thealphacoding@gmail.com",
    description="This package can create Patterns in all A to Z shapes and many more patterns ...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires = [''],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)