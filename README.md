pyvcproj [![Build Status](https://travis-ci.org/jhandley/pyvcproj.svg)](https://travis-ci.org/jhandley/pyvcproj)
========

Manipulate Visual Studio project and solution files from Python.
Currently only tested with Visual Studio 2010.

## Installing

setup.py install

## Usage

Getting project files from a solution:

```python
import vcproj.solution

solution = vcproj.solution.parse('path/to/my/solution.sln')
for project_file in solution.project_files():
	print project_file
```

Getting source and include files from a project_file:

```python
import vcproj.project

project = vcproj.project.parse('path/to/my/project.vcxproj')
for source_file in project.source_files():
    print source_file
for include_file in project.include_files():
    print include_file
```


