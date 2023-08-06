from setuptools import setup, find_packages

setup(
    name='CLIWeb',
    version='0.0.2',
    url='https://github.com/iiestIT/CLIWeb',
    license='MIT',
    author='iiestIT',
    author_email='it.iiest.de@gmail.com',
    description='A cli-tool to performe http requests and socket connections.',
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={"console_scripts": ["cliweb=CLIWeb.cliweb:run"]}
)
