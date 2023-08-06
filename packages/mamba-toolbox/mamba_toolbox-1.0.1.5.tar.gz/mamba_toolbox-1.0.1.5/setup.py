from setuptools import setup, find_packages

setup(
    name="mamba_toolbox",
    version="1.0.1.5",
    description="Mambalib toolbox",
    install_requires=['click==7.1.2'],
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'mamba = mamba.__main__:cli'
        ]
    }
)