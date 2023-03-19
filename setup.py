from setuptools import setup, find_namespace_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="tai",
    version="0.1.0",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'tai = tai:main',
        ],
    },
    install_requires=requirements,
)
