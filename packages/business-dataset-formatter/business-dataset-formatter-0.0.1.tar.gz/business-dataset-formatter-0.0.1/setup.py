import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="business-dataset-formatter",
    version="0.0.1",
    author="Everton Lucas",
    author_email="evtlucas@gmail.com",
    description="A simple dataset formatter based on business days and weekends.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evtlucas/business_dataset_formatter",
    packages=['bdf'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose']
)