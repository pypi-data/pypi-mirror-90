import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gan_recover",
    version="0.0.11",
    author="Tu Meo",
    author_email="tumeotl@gmail.com",
    description="A small package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        'PyYAML',
        'pandas==0.23.3',
        'numpy>=1.14.5',
        'matplotlib>=2.2.0',
        'jupyter'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)