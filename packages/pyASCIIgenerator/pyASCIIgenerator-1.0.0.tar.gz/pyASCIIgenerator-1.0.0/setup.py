from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='pyASCIIgenerator',
    version='1.0.0',
    description='A simple image-to-ASCII converter based on a video by Kite',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/HYKANTUS/pyASCIIgenerator',
    author='HYKANTUS',
    author_email='hykantus@gmail.com',

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
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='ASCII, image, ASCIIart, ASCII art, ASCIIimage, ASCII image, image, art, fun, Pillow, PIL, PIL Image',
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=['pillow'],
    project_urls={
        'Personal Website': 'http://hykantus.tk/',
        'Source': 'https://github.com/HYKANTUS/pyASCIIgenerator/',
    },
)
