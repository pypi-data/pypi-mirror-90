from setuptools import setup, find_packages

setup(
    name='fdmclass',
    version='0.1.2',
    author='fdmseven',
    author_email='wrp2003000@163.com',
    packages=["fdmclass"],
    url='https://github.com/fdmseven/fdmclass',
    license='LICENSE.txt',
    description='independent class',
    long_description=open('README.md').read(),
    python_requires='>=3',
    install_requires=[
        "fdmutils==0.1.2",
    ],
)
