from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='Nyahentai-API',
    version='1.0.0',
    description='Nyahentai Python API made using webscraping.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/AlexandreSenpai/Nyahentai-API',
    author='AlexandreSenpai',
    author_email='alexandrebsramos@hotmail.com',
    keywords='nyahentai hentai AlexandreSenpai',
    license='MIT',
    packages=['nyahentai', 'nyahentai.entities'],
    install_requires=['requests', 'beautifulsoup4'],
    include_package_data=True,
    zip_safe=False
)