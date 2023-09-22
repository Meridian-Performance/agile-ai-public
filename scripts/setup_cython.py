from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

with open("README.md", "r") as fh:
    long_description = fh.read()

# All module name should be fully qualified
# All path should be fully qualified starting at the python_ml
# your include_dirs must contains the '.' for setup to search all the subfolder of the python_ml

base_kwargs = dict()

numpy_kwargs = dict(
    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    include_dirs=['.', numpy.get_include()],
    language="c++",
)

numpy_kwargs.update(base_kwargs)

ext_modules = [
    Extension("agile_ai.cythonized.cat", ["agile_ai/cythonized/cat.pyx"], include_dirs=['.'], language="c++"),
    Extension("agile_ai.cythonized.dog", ["agile_ai/cythonized/dog.pyx"], include_dirs=['.'], language="c++"),
]

for e in ext_modules:
    e.compiler_directives = {'language_level': "3str"}

    
setup(
    name="agile_ai",
    version="0.0.1",
    author="Agile Ai",
    author_email="cody@agil-ai.io",
    description="Agile AI",
    long_description=long_description,
    url="https://github.com/kedifei/agile-ai",
    packages=["agile_ai"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    script_args=['build_ext'],
    options={'build_ext':{'inplace':True, 'force':True}}
)
# compiler_directives={'language_level': "3str"}

print('********CYTHON COMPLETE******')
