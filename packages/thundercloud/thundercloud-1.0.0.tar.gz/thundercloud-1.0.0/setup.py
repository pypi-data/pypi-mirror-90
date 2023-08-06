from setuptools import setup, find_packages

long_description1 = 'This runs your python files on an EC2 Instance!'

setup(
    name = 'thundercloud',
    version = '1.0.0',
    author = 'William Tai',
    author_email = 'williamtai777@gmail.com',
    url = 'https://github.com/wtai777',
    description = 'Runs python files on EC2 instance!',
    long_description = long_description1,
    license = 'BS',
    entry_points = {
        'console_scripts': [
            'thundercloud = thundercloud.main:main'
        ]
    }
)