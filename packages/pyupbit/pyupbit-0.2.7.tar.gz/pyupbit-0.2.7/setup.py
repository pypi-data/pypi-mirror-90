import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyupbit',
    version='0.2.7',
    author='Lukas Yoo, Brayden Jo',
    author_email='brayden.jo@outlook.com, jonghun.yoo@outlook.com, pyquant@outlook.com',
    description='python wrapper for Upbit API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sharebook-kr/pyupbit',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
