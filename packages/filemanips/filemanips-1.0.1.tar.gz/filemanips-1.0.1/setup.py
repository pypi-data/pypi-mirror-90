import setuptools
import zetuptools

TOOLS = zetuptools.SetuptoolsExtensions(
    "filemanips", "Zeke Marffy", "zmarffy@yahoo.com")


setuptools.setup(
    name=TOOLS.name,
    version=TOOLS.version,
    author=TOOLS.author,
    author_email=TOOLS.author_email,
    packages=setuptools.find_packages(),
    url='https://github.com/zmarffy/filemanips',
    license='MIT',
    description='File manipulation functions',
    python_requires=TOOLS.minimum_version_required,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "zetuptools>=2.3.0"
    ],
)
