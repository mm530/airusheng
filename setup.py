from setuptools import setup

PACKAGES = [
    'airusheng',
]

REQUIRES = [
    'lxml',
    'numpy',
    'pika',
    'Pillow',
    'requests',
]

setup(
    name='mm530',
    version='1.0.1',
    description='',
    long_description='',
    author='mm530',
    author_email='mm5303344@163.com',
    url='https://github.com/mm530/airusheng',
    include_package_data=True,
    install_requires=REQUIRES,
    zip_safe=False,
    packages=PACKAGES,
)
