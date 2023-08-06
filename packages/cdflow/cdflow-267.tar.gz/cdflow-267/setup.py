from setuptools import setup
import os


with open(os.path.join(os.getcwd(), 'README.md')) as f:
    long_description = f.read()


setup(
    name='cdflow',
    version='267',
    scripts=['cdflow.py'],
    entry_points={
        'console_scripts': [
            'cdflow = cdflow:run',
        ],
    },
    install_requires=[
        'boto3',
        'docker',
        'pyyaml>=4.2b1',
        'dockerpty',
    ],
    author='Acuris',
    author_email='platform@acuris.com',
    description='Deployment tooling for continuous delivery',
    long_description=long_description,
    long_description_content_type='text/markdown',
    data_files=[('man/man1', ['cdflow.1'])],
    keywords='continuous delivery terraform',
    url='https://mergermarket.github.io/cdflow',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
)
