from setuptools import setup

setup(
    name='idemplus',
    version='0.1',
    description='A python package for minplus and maxplus algebras.',
    url='https://github.com/Cynical314/idemplus',
    author='Franco Formicola',
    author_email='black.franco.formicola@gmail.com',
    license='Apache 2.0',
    packages=['idemplus'],
    zip_safe=False,
    install_requires=[
        'concepts==0.9.1',
        'numpy==1.18.2',
        'pandas==1.0.3'
    ]
)
