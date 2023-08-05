import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sokrato",
    version="0.0.1",
    author="Sokrato",
    author_email="sokrato@outlook.com",
    description="Commonly used utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sokrato/repo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests>=2.25.1,<3'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'sokrato=sokrato.cli:main',
        ],
    },
)