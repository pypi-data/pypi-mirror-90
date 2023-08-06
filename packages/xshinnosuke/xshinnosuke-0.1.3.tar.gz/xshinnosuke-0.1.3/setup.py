import setuptools

with open("xshinnosuke/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xshinnosuke", # Replace with your own username
    version="0.1.3",
    author="Eleven",
    author_email="eleven_1111@outlook.com",
    description="Deep learning framework realized by Numpy purely, supports for both Dynamic Graph and Static Graph with GPU acceleration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/E1eveNn/xshinnosuke",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
