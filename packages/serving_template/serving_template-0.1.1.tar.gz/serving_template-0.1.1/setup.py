from setuptools import setup, find_packages
from codecs import open
from os import path
import glob

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get all files of templates recursively
def package_dir(pkg_name, dir_name):
    pkg_path = path.join(here, pkg_name)
    dir_path = path.join(pkg_path, dir_name, '**')
    files = []
    for entry in glob.glob(dir_path, recursive=True):
        files.append(entry[len(pkg_path) + 1 :])
    return files


setup(
    name='serving_template',
    version='0.1.1',
    description='Model Serving Project Template',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/HughWen/ServingTemplate',
    author='wwen',
    author_email='wenwh@mail.sustech.edu.cn',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='model serving template',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['click', 'sh'],
    python_requires='>=3',
    extras_require={'dev': ['check-manifest'], 'test': ['coverage'],},
    package_data={'serving_template': package_dir('serving_template', 'templates'),},
    entry_points={'console_scripts': ['serving_template=serving_template.main:cli',],},
)

