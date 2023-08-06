import io
from setuptools import setup
from setuptools.extension import Extension
import versioneer

with io.open('README.md', encoding='utf_8') as fp:
    readme = fp.read()

setup(
    author="Rajesh Prabhu",
    author_email="",
    name='textcloud',
    version='0.0.3',
    #cmdclass=versioneer.get_cmdclass(),
    url='https://github.com/eRajsh/text_cloud',
    description="A little text cloud generator, based on AMueller's excellent word cloud",
    long_description=readme,
    long_description_content_type='text/markdown; charset=UTF-8',
    license='MIT',
    install_requires=['numpy>=1.6.1', 'pillow', 'matplotlib'],
    ext_modules=[Extension("textcloud.query_integral_image",
                           ["textcloud/query_integral_image.c"])],
    entry_points={'console_scripts': ['textcloud_cli=textcloud.__main__:main']},
    packages=['textcloud'],
    package_data={'textcloud': ['stopwords', 'MuseoModerno-SemiBold.ttf']}
)
