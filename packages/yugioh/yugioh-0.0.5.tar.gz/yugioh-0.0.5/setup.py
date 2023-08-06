import setuptools

def readme():
    with open('README.md') as f:
        return f.read()
        
setuptools.setup(name='yugioh',
                 py_modules=["yugioh"],
                 entry_points={"console_scripts": ["yugioh=clt:main"]},
                 version='0.0.5',
                 description='Yu-Gi-Oh API Wrapper & CLT',
                 long_description=readme(),
                 long_description_content_type='text/markdown',
                 url='https://github.com/pclt-dev/yugioh',
                 author='diogenesjunior',
                 author_email='diogenesjunior@protonmail.com',
                 packages=['yugioh'],
                 keywords='Yu-Gi-Oh API')
