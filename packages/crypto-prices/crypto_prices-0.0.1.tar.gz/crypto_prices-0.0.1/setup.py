from setuptools import setup, find_packages

setup(
    name='crypto_prices',
    packages=find_packages(),
    version='0.0.1',
    description="Get daily/hourly/minutely Crypto prices",
    long_description='README.md',
    author = 'Ali Siddiq',
    author_email = 'ali.bin.siddiq@gmail.com',
    url = 'https://github.com/alisiddiq/crypto_prices',
    license='MIT',
    keywords = ['crypto', 'prices'],
    install_requires = ['pandas', 'requests', 'tqdm'],
)