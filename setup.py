from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='waylandmap',
    packages=['waylandmap', ],
    version='1.0.0',
    description='A keymapper that works under both X11 or Wayland',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Quantum Snowball',
    author_email='quantum.snowball@gmail.com',
    url='https://github.com/quantumsnowball/waylandmap',
    keywords=['wayland', 'keymappers', 'evdev', 'python-uinput', ],
    python_requires='>=3.6',
    install_requires=['click', 'evdev', 'python-uinput', 'pyyaml' ],
    entry_points={
        'console_scripts': [
            'waylandmap=waylandmap.main:cli',
        ]
    }
)

