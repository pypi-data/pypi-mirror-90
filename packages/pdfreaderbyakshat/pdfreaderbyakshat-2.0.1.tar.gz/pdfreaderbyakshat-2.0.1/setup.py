import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdfreaderbyakshat", # Replace with your own username
    version="2.0.1",
    author="Akshat Tiwari",
    author_email="thealphacoding@gmail.com",
    description="A small example package",
    long_description="long_description",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)
