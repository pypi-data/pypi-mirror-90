from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name                ='getwallpapers',
    packages            =find_packages(include=['getwallpapers']),
    version             ='0.1.1',
    description         ='download wallpaper collection from http://getwallpapers.com/',
    long_description    = long_description,
    long_description_content_type='text/markdown',
    author              ='Shrikrishna Joisa',
    author_email        ='shrikrishnajois@gmail.com',
    license             ='MIT',
    url                 ='https://github.com/falcon-head/getwallpapers-downloader',
    platforms           =['Any'],
    py_modules          =[],
    install_requires    =['beautifulsoup4', 'tqdm', 'urllib3'],
    classifiers         =[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)