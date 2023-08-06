import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="creatio-connector-sumarokov",
    version="0.0.1",
    author="Vladimir Sumarokov",
    author_email="sumarokov.vp@gmail.com",
    description="Connector to your Creatio project (https://www.creatio.com)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sumarokov-vp/py_creatio_connector",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)