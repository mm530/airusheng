from setuptools import setup

PACKAGES = [
    'lemon',
]

REQUIRES = [
    'lxml',
    'numpy',
    'pika',
    'Pillow',
    'requests',
]

setup(
    name='lemon',
    version='1.0.1',
    description='',
    long_description='',
    author='mm530',
    author_email='mm5303344@163.com',
    url='https://github.com/mm530/lemon',
    include_package_data=True,
    install_requires=REQUIRES,
    zip_safe=False,
    packages=PACKAGES,
)
