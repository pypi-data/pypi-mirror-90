from setuptools import setup, find_packages

setup(name='gym_vim',
    version='0.0.3',
    find_packages=find_packages(),
    install_requires=['gym', 'sklearn', 'numpy', 'pynvim']  # And any other dependencies foo needs
)
