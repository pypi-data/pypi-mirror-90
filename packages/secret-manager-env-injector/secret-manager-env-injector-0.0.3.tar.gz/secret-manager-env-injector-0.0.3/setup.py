import setuptools

def read(fname):
    """ Return file content. """
    with open(fname) as f:
        content = f.read()

    return content

description = "A plug-n-play package fetch secrets form secret manager and insert them in the env"
try:
    long_description = read('README.MD')
except IOError:
    long_description = description

setuptools.setup(
    name="secret-manager-env-injector",
    package=['secret-manager-env-injector'],
    version="0.0.3",
    author="Bharat Sinha",
    author_email="bharat.sinha.2307@gmail.com",
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Bharat23/secret-manager-env-injector",
    packages=setuptools.find_packages(),
    license='MIT',
    keywords = ['AWS', 'secret manager', 'env', 'cloud', 'json'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
    ],
    install_requires=[
          'boto3',
      ],
    python_requires='>=3.6',
)
