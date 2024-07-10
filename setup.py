from setuptools import setup, find_packages

setup(
    name='expenses_tracker_backend',  # Replace with your project name
    version='0.1.0',
    description='A detached backend to the main application',
    author='Francesco',
    author_email='ngr.francesco@gmail.com',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        "numpy"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ],
)