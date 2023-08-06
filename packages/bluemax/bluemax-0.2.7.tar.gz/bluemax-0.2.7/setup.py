from setuptools import setup, find_packages

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = True


except ImportError:
    bdist_wheel = None


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="bluemax",
    version="0.2.7",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/blueshed/bluemax/",
    packages=find_packages(exclude=["tests.*", "tests", "foo.*"]),
    package_data={"bluemax.web": ["static/*"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["tornado", "invoke", "pyyaml"],
    extras_require={
        "sa": ["alembic"],
        "redis": ["aioredis"],
        "all": ["alembic", "aioredis"],
        "dev": [
            "alembic",
            "aioredis",
            "wheel",
            "twine",
            "bumpversion",
            "pytest-tornasync",
            "pytest-cov",
            "lovely-pytest-docker",
            "pytest-benchmark",
            "flake8",
            "ldap3",
            "ipython",
        ],
    },
    entry_points={"console_scripts": ["bluemax=bluemax.tasks:program.run"]},
)
