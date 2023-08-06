import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='to-ascii',
    version='3.5.8',
    author='Iapetus-11',
    description='A package which can convert videos, images, gifs, and even live video to ascii art!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Iapetus-11/to-ascii',
    packages=setuptools.find_packages(),
    install_requires=[
        'opencv-python'
    ],
    data_files=[
        ('', ['LICENSE'])
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['to-ascii=toascii.CLI:main']
    }
)
