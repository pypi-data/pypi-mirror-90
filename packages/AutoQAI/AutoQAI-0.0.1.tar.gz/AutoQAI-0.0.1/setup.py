import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AutoQAI",
    version="0.0.1",
    author="rvk",
    author_email="rvk.vamshi@gmail.com",
    description="A Quantum Artificial Intelligence Workplace",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vamshi-rvk/AutoQAI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
