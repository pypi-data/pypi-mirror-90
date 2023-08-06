import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="interactive-data-manipulation", # Replace with your own username
    version="0.0.1",
    author="ChuanSun",
    author_email="chuansun.sc@gmail.com",
    description="A library for Jupyter notebook interactive data manipulations",
    long_description="A library for Jupyter notebook interactive data manipulations",
    long_description_content_type="text/markdown",
    url="https://github.com/telenovelachuan/interactive_data_manipulation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)