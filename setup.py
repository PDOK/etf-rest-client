from setuptools import setup

version = "0.1.dev0"

long_description = "\n\n".join([open("README.md").read(), open("CHANGES.md").read()])

install_requires = []

tests_require = ["pytest", "mock", "pytest-cov", "pytest-flakes", "pytest-black"]

setup(
    name="etf-rest-client",
    version=version,
    description="Client library to interact with RESTful API of ETF validator",
    long_description=long_description,
    # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=["Programming Language :: Python", "Framework :: Django"],
    keywords=[],
    author="Anton Bakker",
    author_email="anton.bakker@kadaster.nl",
    url="https://github.com/ordina-pythoneers/etf-rest-client",
    license="MIT",
    packages=["etf_rest_client"],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={"test": tests_require},
    entry_points={
        "console_scripts": [
            "run-etf-rest-client = etf_rest_client.scripts:main"
        ]
    },
)
