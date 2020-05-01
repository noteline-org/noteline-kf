import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noteline-kf",
    version="0.1.0",
    author="Viacheslav Kovalevskyi",
    author_email="viacheslav@kovalevskyi.com",
    description="Noteline Kubeflow Pipeline step for executing Notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noteline-org/noteline-kf",
    packages=setuptools.find_packages(),
    install_requires=[
        'kfp'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)