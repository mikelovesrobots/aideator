from setuptools import setup, find_namespace_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='tai',
    version='0.1.0',
    description='TAI (text artisan interface) is a productivity command-line tool that uses openai tools for text transformations',
    url='http://github.com/mikelovesrobots/tai',
    author='Mike Judge',
    author_email='mikelovesrobota+tais@gmail.com',
    license='MIT',
    packages=['tai'],
    zip_safe=False,
    entry_points={
        'console_scripts': [ 'tai = tai:cli' ],
    },
    install_requires=requirements
)
