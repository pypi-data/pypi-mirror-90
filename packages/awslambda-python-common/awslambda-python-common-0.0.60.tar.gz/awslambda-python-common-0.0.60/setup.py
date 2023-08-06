import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="awslambda-python-common", 
    version="0.0.60",
    author="Lawrence M",
    author_email="lawrence.mok@gmail.com",
    description="AWS Lambda Python development framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/lm-private/awslambda-python-common",
    packages=setuptools.find_packages(
        where="src/main"
    ),
    package_dir={
        "": "src/main/"
    },
    install_requires=[
        "pyjwt",
        "dacite",
        "aws_lambda_powertools"
    ],
    python_requires='>=3.6'
)