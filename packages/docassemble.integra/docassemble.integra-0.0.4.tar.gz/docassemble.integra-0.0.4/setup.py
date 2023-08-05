import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="docassemble.integra",
    version="0.0.4",
    author="Alexey Breusov",
    author_email="alexeybreusov5@gmail.com",
    description="Generate a signed smart document",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexeybreusov5/SmartDocument",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)