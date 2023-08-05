#!/usr/bin/env python

from distutils.core import setup, Extension
from os import system, environ
from os.path import abspath, dirname, exists
from sys import platform


# set path variables
v8eval_root = abspath(dirname(__file__))
v8_dir = v8eval_root + '/v8'
py_dir = v8eval_root + '/python'
py_v8eval_dir = py_dir + '/v8eval'


# install v8 and build libv8eval.a
system(v8eval_root + '/build.sh')


# generate v8eval_wrap.cxx and v8eval.py
system('cp ' + v8eval_root + '/src/v8eval.h ' + py_v8eval_dir)
system('cp ' + v8eval_root + '/src/v8eval_python.h ' + py_v8eval_dir)
system('swig -c++ -python -outdir ' + py_v8eval_dir + ' -o '  + py_v8eval_dir + '/v8eval_wrap.cxx ' + py_v8eval_dir + '/v8eval.i')
system('cat ' + py_dir + '/_v8eval.py >> ' + py_v8eval_dir + '/v8eval.py')


# build _v8eval.so
if platform == 'linux' or platform == 'linux2':
    environ['CC'] = v8_dir + '/third_party/llvm-build/Release+Asserts/bin/clang'
    environ['CXX'] = v8_dir + '/third_party/llvm-build/Release+Asserts/bin/clang++'
    environ['PATH'] = v8_dir + '/third_party/binutils/Linux_x64/Release/bin:' + environ['PATH']

include_dirs = [v8_dir, v8_dir + '/include']
library_dirs = [v8eval_root + '/build', v8_dir + '/out.gn/x64.release/obj']
libraries=['v8eval',
           'v8eval_python',
           'v8_libplatform',
           'v8_base',
           'v8_libbase',
           'v8_libsampler',
           'v8_init',
           'v8_initializers',
           'v8_nosnapshot',
           'torque_generated_initializers']
extra_compile_args=['-O3', '-std=c++14', '-stdlib=libc++']

if platform == 'linux' or platform == 'linux2':
    library_dirs += [v8_dir + '/out.gn/x64.release/obj/buildtools/third_party/libc++',
                     v8_dir + '/out.gn/x64.release/obj/buildtools/third_party/libc++abi']
    libraries += ['rt', 'c++', 'c++abi']
    extra_compile_args += ['-isystem' + v8_dir + '/buildtools/third_party/libc++/trunk/include',
                           '-isystem' + v8_dir + '/buildtools/third_party/libc++abi/trunk/include']

v8eval_module = Extension(
    '_v8eval',
    sources=[py_v8eval_dir + '/v8eval_wrap.cxx'],
    libraries=libraries,
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    extra_compile_args=extra_compile_args)


# make description
description = 'Run JavaScript engine V8 in Python'
long_description = description
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    pass


# workaround
system("rm -rf " + v8_dir + "/third_party/perfetto")
system("mkdir " + v8_dir + "/buildtools/third_party/libc++/trunk/test/std/experimental/filesystem/Inputs/static_test_env/dne")


# setup v8eval package
setup(name='v8eval',
      version='0.3.2',
      author='Yoshiyuki Mineo',
      author_email='Yoshiyuki.Mineo@sony.com',
      license='MIT',
      url='https://github.com/sony/v8eval',
      description=description,
      long_description=long_description,
      keywords='v8 js javascript binding',
      ext_modules=[v8eval_module],
      py_modules=['v8eval'],
      package_dir={'': 'python/v8eval'},
      classifiers=['License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: Implementation :: CPython',
                   'Operating System :: POSIX :: Linux',
                   'Operating System :: MacOS :: MacOS X',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries'])
