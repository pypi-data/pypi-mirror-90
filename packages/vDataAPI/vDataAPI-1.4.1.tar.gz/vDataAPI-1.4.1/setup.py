from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='vDataAPI',
    packages=find_packages(include=["vDataAPI"]),
    install_requires=['requests==2.25.1'],
    version='1.4.1',
    description='vData.PL - API Client in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="HSCode.PL",
    license="MIT",
    url="https://gitlab.com/hscode/vdataapi-python/",
    keywords=['vData.pl', 'HSCode.PL', 'API'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Natural Language :: Polish',
        'Natural Language :: English'
    ],
)
