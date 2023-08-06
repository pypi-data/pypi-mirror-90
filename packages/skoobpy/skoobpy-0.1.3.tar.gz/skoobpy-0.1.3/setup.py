from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name                ='skoobpy',
    packages            =find_packages(include=['skoobpy']),
    version             ='0.1.3',
    description         ='extracts user\'s desired books from Skoob.com.br',
    long_description    = long_description,
    long_description_content_type='text/markdown',
    author              ='Diego Lourenço',
    author_email        ='diego.lourenco15@gmail.com',
    license             ='MIT',
    url                 ='https://github.com/Diegoslourenco/skoobpy',
    platforms           =['Any'],
    py_modules          =['skoobpy'],
    install_requires    =[],
    classifiers         =[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)