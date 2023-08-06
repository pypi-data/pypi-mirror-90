from setuptools import setup

setup(
    name='py_VOD',
    version='0.4.0',
    packages=['pyvod'],
    url='https://github.com/OpenJarbas/pyvod/',
    license='Apache',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    include_package_data=True,
    install_requires=["requests", "youtube-dl", "pafy", "json_database"],
    description='video on demand'
)
