from setuptools import setup, find_packages

setup(
    name="mpip",
    version='0.1.2',
    license='MIT',
    url="https://github.com/jjorissen52/mpip",

    description="mpip is a thin wrapper around pip which helps you manage your project requirements.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    author='John-Paul Jorissen',
    author_email='jjorissen52@gmail.com',

    keywords='python pip requirements requirements.txt project management',

    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mpip = mpip.mpip:main",
        ],
    },
    install_requires=["fire", "rich", "execution-pipeline"],
)
