import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='autobean',
    version='0.1.0',
    author='SEIAROTg',
    author_email='seiarotg@gmail.com',
    description='A collection of plugins and scripts that help automating bookkeeping with beancount',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SEIAROTg/autobean',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Topic :: Office/Business :: Financial :: Accounting',
    ],
    python_requires='>=3.5',
)
