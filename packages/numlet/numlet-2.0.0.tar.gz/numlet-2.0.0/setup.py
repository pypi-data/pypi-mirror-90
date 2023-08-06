from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="numlet",
    version="2.0.0",
    author="Roylan Martinez Vargas",
    author_email="roylanmartinez97@gmail.com",
    description="Convierte a letras más de 10^600 números",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/roylanmartinez/Numlet",
    packages=['nlt'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
