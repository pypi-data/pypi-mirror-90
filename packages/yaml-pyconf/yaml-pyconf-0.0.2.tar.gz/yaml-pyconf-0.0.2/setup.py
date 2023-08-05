import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="yaml-pyconf",
    version="0.0.2",
    author="Gabrielle Sloane Law",
    author_email="rockymcrockerson@gmail.com",
    description="Turn YAML files into python objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gabriellesw/yaml-pyconf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Topic :: Utilities",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.6",
    install_requires=["python-dotenv", "PyYAML"],
    test_suite="tests",
    package_data={
        "yaml_pyconf": [
            "samples/sample-yaml/*.yaml",
            "samples/sample-dotenv/.env",
        ]
    },
)
