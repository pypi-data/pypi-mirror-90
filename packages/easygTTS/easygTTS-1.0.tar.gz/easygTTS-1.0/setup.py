from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='easygTTS',
    packages=['easygTTS'],
    version='1.0',
    license='MIT',
    description='Easy async interface to easy-gtts-api',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Gnome-py',
    author_email='gnome6669.py@gmail.com',
    url='https://github.com/gnome-py/py-easygTTS',
    download_url='https://github.com/Gnome-py/py-easygTTS/archive/v1.0.tar.gz',
    keywords=['async', 'TTS', 'gtts', 'text to speech'],
    install_requires=['aiohttp'],
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    ],
)   
