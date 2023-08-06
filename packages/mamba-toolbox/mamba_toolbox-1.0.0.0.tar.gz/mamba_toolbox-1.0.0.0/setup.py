from mamba.__main__ import __version__
     
from setuptools import setup, find_packages

setup(
    name="mamba_toolbox",
    version=".".join(str(x) for x in __version__),
    description="Mambalib toolbox",
    install_requires=['click==7.1.2'],
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'mamba = mamba.__main__:cli'
        ]
    }
)