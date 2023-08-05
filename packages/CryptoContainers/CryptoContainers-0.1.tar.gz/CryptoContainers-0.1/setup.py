from setuptools import setup

setup(
    name="CryptoContainers",
    version=0.1,
    author="Lightman",
    author_email="L1ghtM3n@protonmail.com",
    description="Python module for secure, encrypted file storage",
    url="https://github.com/L1ghtM4n/CryptoContainer",
    packages=["CryptoContainers"],
    install_requires=[
        "pycryptodome"
      ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)