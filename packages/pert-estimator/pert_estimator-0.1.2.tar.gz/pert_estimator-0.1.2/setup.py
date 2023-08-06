from setuptools import setup


with open('README.md') as f:
    readme = f.read()

setup(
    name='pert_estimator',
    version='0.01.2',
    license='MIT',
    description='PERT estimation tool',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Andrew Dieken',
    author_email='andrewrd@live.com',
    url='https://github.com/andrewdieken/pert_estimator',
    keywords=['pert', 'estimator', 'ticket', 'story'],
    packages=['pert_estimator'],
    install_requires=['prettytable'],
    entry_points={
        'console_scripts': [
            'pert_estimator = pert_estimator.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)