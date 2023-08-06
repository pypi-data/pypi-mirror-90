from setuptools import setup, find_packages
import pggui
setup(
    name="pggui",
    version=pggui.__version__,
    packages=find_packages(),
    author="LavaPower",
    author_email="lavapower84@gmail.com",
    description="A lib to make GUI made with PyGame",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    include_package_data=True,
    url='https://github.com/AlexisHuvier/PGGUI',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        'Intended Audience :: Developers'
    ],
    install_requires=["pygame"]
)