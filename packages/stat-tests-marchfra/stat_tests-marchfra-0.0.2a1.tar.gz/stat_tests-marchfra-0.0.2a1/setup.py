import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stat_tests-marchfra",
    version="0.0.2.a1",
    author="marchfra",
    author_email="marchfra1@gmail.com",
    description="A package that performs statistical tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marchfra/stat-tests.git",
    packages=setuptools.find_packages(include=['stat_tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.1',
    install_requires=['sympy', 'uncertainties'],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)