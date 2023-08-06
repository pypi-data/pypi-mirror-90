import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data_science_pipeline_automation",
    version="0.0.2",
    author="@chizhangucb",
    author_email="chizhangucb@gmail.com",
    description="Python library to help you to automate the data science pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chizhangucb/data_science_pipeline_automation",
    install_requires=[
        "pandas>=1.1", "numpy", "scipy", "sklearn", "altair", "IPython",
        "lightgbm", "xgboost", "gbm_autosplit>=0.0.2", "networkx"
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
