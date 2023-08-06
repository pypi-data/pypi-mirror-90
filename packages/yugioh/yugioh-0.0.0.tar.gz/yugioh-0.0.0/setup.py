import setuptools

def readme():
    with open('README.rst') as f:
        return f.read()
        
setuptools.setup(name='yugioh',
                 version='0.0.0',
                 description='Yu-Gi-Oh API Wrapper',
                 long_description=readme(),
                 url='https://github.com/pclt-dev/yugioh',
                 author='diogenesjunior',
                 author_email='diogenesjunior@protonmail.com',
                 packages=['yugioh'],
                 zip_safe=False,
                 keywords='Yu-Gi-Oh API',
                 include_package_data=True)
