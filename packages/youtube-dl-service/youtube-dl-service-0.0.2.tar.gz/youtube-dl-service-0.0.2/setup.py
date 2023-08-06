from setuptools import setup


with open('README.md', 'r') as f:
    readme = f.read()


if __name__ == '__main__':
    setup(
        name='youtube-dl-service',
        version='0.0.2',
        author='Dmitriy Pleshevskiy',
        author_email='dmitriy@ideascup.me',
        description='Using youtube-dl as service in python code',
        long_description=readme,
        long_description_content_type='text/markdown',
        package_data={'': ['LICENSE', 'README.md']},
        include_package_data=True,
        license='MIT',
        packages=['youtube_dl_service'],
        install_requires=[
            'youtube-dl==2020.12.29',
        ]
    )