from setuptools import setup, find_packages

setup(
    name='SQLInjectionFirewall',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'SQLAlchemy',
    ],
    entry_points={
        'console_scripts': [
            'sqlinjectionfirewall=SQLInjectionFirewall.app:main',
        ],
    },
    author='Votre Nom',
    author_email='votre_email@example.com',
    description='Un pare-feu basique pour détecter et prévenir les injections SQL dans une application web Flask.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/votre_utilisateur/SQLInjectionFirewall',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
