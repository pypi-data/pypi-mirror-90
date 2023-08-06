import setuptools

setuptools.setup(
    name='django-timedelta',
    version='2020.12.30',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
