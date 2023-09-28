Python package structure recommendation

https://docs.python-guide.org/writing/structure/
https://kennethreitz.org/essays/2013/01/27/repository-structure-and-python

Good post on importing
import submodules in \_\_init\_\_.py to make them importable from other packages (See Numpy example in:)
https://note.nkmk.me/en/python-import-usage/#packages

another good post on importing
https://fortierq.github.io/python-import
sys.path seems a clunky solution... may be useful when writing tests, though
relative paths
do you intend to build/install or run as script?

see also
https://blog.finxter.com/python-how-to-import-modules-from-another-folder/
https://ioflood.com/blog/python-import-from-another-directory/

"namespace packages" are the new tech, but may create confusion and seem best for advanced cases where sub-packages are distributed across different directories in teh filesystem and will be "re assembled" at run time

https://peps.python.org/pep-0420/

with relative imports and packages with blank \_\_init\_\_.py files, "python -m dbapp" works but "python dbapp/\_\_main\_\_.py" fails due to " ImportError: attempted relative import with no known parent package "


From chatgpt:

Whether you should use namespace packages or regular packages in your Python project depends on your project's specific requirements and goals. Both namespace packages and regular packages have their use cases, and understanding the differences between them can help you make an informed decision.

1. Regular Packages:
   - Regular packages are the most common type of packages in Python.
   - They are used when you want to organize your code into hierarchical directories and create a clear package structure.
   - Regular packages are self-contained and can include modules (Python files) and sub-packages (nested directories with an `__init__.py` file).
   - They provide strong encapsulation, meaning that each regular package is its own namespace, and names within the package do not collide with names in other packages.

   Example:
   ```
   mypackage/
       __init__.py
       module1.py
       module2.py
       subpackage/
           __init__.py
           module3.py
   ```

2. Namespace Packages:
   - Namespace packages are used when you want to split a package across multiple directories or when you want to extend an existing package without modifying its source code.
   - They are more suitable for scenarios where you have multiple packages that share a common namespace and you want to merge them dynamically.
   - Namespace packages do not contain any actual code or `__init__.py` files. They are created by declaring a shared namespace in one or more distribution packages.
   - Names within a namespace package can be spread across multiple locations, and they are merged at runtime.

   Example (project structure with namespace packages):
   ```
   mynamespacepackage/
       subpackage1/
           module1.py
       subpackage2/
           module2.py
   ```

In summary, if you are building a self-contained package with a clear structure and want strong encapsulation, regular packages are a good choice. On the other hand, if you need to extend or split a package dynamically across multiple directories or collaborate on a shared namespace with other packages, namespace packages might be more appropriate.

Consider your project's specific needs and whether you anticipate collaborating with other packages or distributing your code as part of a larger ecosystem when deciding whether to use regular packages or namespace packages.



# Python scripts

* Modules in one directory; no sub-directories
* No \_\_init\_\_.py file
* One file contains the main logic, other modules contain functions

```
project1
├── functions.py
└── program.py
```

functions.py:

```
def func1(message)
    return message + " by func1"
```

program.py

```
import functions

def main():
    print(functions.func1("test"))

if __name__ == "__main__":
    main()
```

Run from project directory:

```
$ cd project1
$ python3 -m program
test by func1
```

```
$ python3 program.py
test by func1
```

Run from another directory

```
$ cd ..
$ python3 -m project1.program
Traceback (most recent call last):
...
  File "/home/brian/Projects/learning/python/imports/project1/program.py", line 1, in <module>
    import functions
ModuleNotFoundError: No module named 'functions'
```

```
$ python3 project1/program.py
test by func1
```

## Python package (normal)

Add an empty file named *\_\_init\_\_.py* and the project directory becomes a *package*. Changes the way imports work. Now you need "relative" or "absolute" imports.

```
project2
├── functions.py
├── __init__.py
└── program.py
```

```
$ cd project2
$ python3 -m program.py
test by func1
```
```
$ python3 program.py
test by func1
```
```
$ cd ..
$ python3 -m project2.program
Traceback (most recent call last):
...
  File "/home/brian/Projects/learning/python/imports/project2/program.py", line 1, in <module>
    import functions
ModuleNotFoundError: No module named 'functions'
```
```
$ python3 project2/program.py
test by func1
```

Seems to work the same as normal script modules.

### Relative imports

To make the case of `python3 -m project2.program` work, you need to use relative imports. *\_\_init\_\_.py* tells python that relative imports are allowed. Also the `python -m` flag tells Python that relative imports are allowed. Relative imports will not wotk when running as a script with `python program.py`

Change *program.py* to:

```
from . import functions

def main():
    print(functions.func1("test"))

if __name__ == "__main__":
    main()
```

The import line was changed to `from . import functions`.

Now, the following works:

```
$ python3 -m project2.program
test by func1
```

The directory *project2* is now a *package* and Python searches for modules starting from the directory containing the *project* package directory, not from the *project2* directory, itself.
???

But the program can no longer be run as a Python script. It must be run as a module with the `-m` flag and it must be run as a package: identified as `project2`:

```
$ python3 project2/program.py
Traceback (most recent call last):
  File "/home/brian/Projects/learning/python/imports/project2/program.py", line 1, in <module>
    from . import functions
ImportError: attempted relative import with no known parent package
```
```
$ cd project2
$ python3 program.py
Traceback (most recent call last):
  File "/home/brian/Projects/learning/python/imports/project2/program.py", line 1, in <module>
    from . import functions
ImportError: attempted relative import with no known parent package
```
```
$ python3 -m program
Traceback (most recent call last):
  File "/usr/lib/python3.10/runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/usr/lib/python3.10/runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "/home/brian/Projects/learning/python/imports/project2/program.py", line 1, in <module>
    from . import functions
ImportError: attempted relative import with no known parent package
```

## Namespace package

You need to keep in mind how you will distribute the program. If you intend to "package" it using something like *setuptools*, then you may need to be careful about the metatdata you generate for the packaging process.
adding some code to the \_\_init\_\_.py file to initialize the Python search path to include the package directory

*\_\_init\_\_.py* would contain:

```
from pathlib import Path
import  sys

print(Path(__file__).parents[0])
path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))
print(sys.path)
```

Now all types of launches run 

```
$ cd project2
$ python3 -m program.py
test by func1
```
```
$ python3 program.py
test by func1
```
```
$ cd ..
$ python -m project2.program
C:\Users\blinklet\Documents\learning\python\imports\project2
test by func1
```

**(Note, the above call to the *project2.program* module caused the */_/_init.py/_/_* code to ruin. None of the other launches started the init file.)**

```
$ python3 project2/program.py
test by func1
```

So, that's one way to make package module imports work for all cases




SQLAlchemy

[declarative mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-declarative-mapping)


https://www.youtube.com/watch?v=XWtj4zLl_tg


where to create session?
"ourside" functions that use it
see: 

used sessionmaker to get automatic connection management
https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker
use session.begin method

from:  https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker
"When you write your application, the sessionmaker factory should be scoped the same as the Engine object created by create_engine(), which is typically at module-level or global scope. As these objects are both factories, they can be used by any number of functions and threads simultaneously."
where?
https://docs.sqlalchemy.org/en/20/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it


how to update a row using ORM instead of "query" class
https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-update-and-delete-with-custom-where-criteria

query class is deprecated
https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html
"In the SQLAlchemy 2.x series, SQL SELECT statements for the ORM are constructed using the same select() construct as is used in Core, which is then invoked in terms of a Session using the Session.execute() method (as are the update() and delete() constructs now used for the ORM-Enabled INSERT, UPDATE, and DELETE statements feature). However, the legacy Query object, which performs these same steps as more of an “all-in-one” object, continues to remain available as a thin facade over this new system, to support applications that were built on the 1.x series without the need for wholesale replacement of all queries. For reference on this object, see the section Legacy Query API."
also see: https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#legacy-query-api


Running a Python program using "python x.py" and "python -m x" can yield different results because they use different ways to execute Python code and have different implications for how modules and packages are treated. Here's an explanation of the differences:

1. "python x.py":
   - When you run "python x.py," you are executing the Python script "x.py" directly as a standalone script.
   - The Python interpreter treats "x.py" as the main program and starts executing code from the top of the file.
   - Any code within "x.py" that is not encapsulated in functions or classes will be executed immediately when you run the script.
   - This method is suitable for standalone scripts and simple programs.

2. "python -m x":
   - When you run "python -m x," you are telling Python to run the module named "x" as a script.
   - In this case, "x" should be a Python package or a module that can be imported.
   - Python will search for the "x" module/package in its module search path, including the current directory.
   - It treats "x" as a package or module and executes the code in the "\_\_main\_\_.py" file inside the "x" package (if it exists), or it runs the module "x" directly if there is no "\_\_main\_\_.py" file.
   - This method is often used for running packages or modules within a larger Python project.

Key Differences:
- The "python -m x" method is typically used for structured Python projects where you want to utilize packages and modules, while "python x.py" is often used for standalone scripts.
- Using "python -m x" allows you to avoid issues related to naming conflicts with other scripts or modules in the same directory or on the Python path.
- When using "python -m x," the "\_\_name\_\_" attribute of the script/module will be "\_\_main\_\_," just like when running a standalone script, so you can still use conditional logic based on "\_\_name\_\_" to control script behavior.

In summary, the choice between "python x.py" and "python -m x" depends on the structure and purpose of your Python code. If it's a simple standalone script, "python x.py" is sufficient. If you're working with modules and packages in a more complex project, "python -m x" is a better choice for running your code as a module.







The error message you're encountering, "ImportError: attempted relative import with no known parent package," is related to the way you are running your Python script and the use of relative imports.

In Python, relative imports are used within packages (directories containing an `__init__.py` file) to reference other modules or sub-packages within the same package. However, when you run a script directly with "python3 .\dbapp\interface\cli.py," Python treats it as a standalone script, not as part of a package, which is why relative imports fail.

To resolve this issue, you have a few options:

1. Run the script as a module with the `-m` flag:

   ```
   python3 -m dbapp.interface.cli
   ```

   This method treats the script as a module within the `dbapp` package and allows you to use relative imports correctly.

2. Change your project structure:

   If you intend to use relative imports within your script, consider organizing your project structure as a package. To do this:

   - Ensure that the top-level directory (`dbproject` in your case) contains an `__init__.py` file. This makes it a Python package.
   - Move your script (`cli.py`) to the appropriate location within the package. For example, if `dbapp` is your package and `cli.py` is a module within it, your directory structure might look like this:

     ```
     dbproject/
     ├── dbapp/
     │   ├── __init__.py
     │   ├── interface/
     │   │   ├── __init__.py
     │   │   └── cli.py
     ├── ...
     ```

   With this structure, you can run your script as a module with relative imports:

   ```
   python3 -m dbapp.interface.cli
   ```

3. Use absolute imports:

   Instead of relying on relative imports, you can use absolute imports by specifying the full path to the module you want to import. For example:

   ```python
   from dbapp.interface import db
   ```

   This approach works both when running the script as a standalone file and when using it as a module.

Choose the approach that best fits your project structure and requirements. If you intend to work with packages and modules within your project, I recommend organizing your project as a package to leverage the benefits of relative imports and better code organization.



References??

Certainly! Here are some reference links that provide more information on the topics discussed:

1. **Python Official Documentation**:
   - [Python Modules](https://docs.python.org/3/tutorial/modules.html)
   - [Packages](https://docs.python.org/3/tutorial/modules.html#packages)
   - [Command line and environment](https://docs.python.org/3/using/cmdline.html)

2. **PEP 328 - Imports: Multi-Line and Absolute/Relative**:
   - [PEP 328](https://www.python.org/dev/peps/pep-0328/) explains the rationale behind relative imports and their usage.

3. **Python Module vs. Script**:
   - [Python Module vs. Script](https://realpython.com/run-python-scripts/) - An article explaining the differences between running Python modules and scripts.

4. **Structuring Your Project**:
   - [Structuring Your Project](https://docs.python-guide.org/writing/structure/) - A guide on structuring Python projects, including the use of packages and modules.

5. **Absolute vs. Relative Imports in Python**:
   - [Absolute vs. Relative Imports in Python](https://realpython.com/absolute-vs-relative-python-imports/) - A Real Python article that delves into the details of absolute and relative imports in Python.

6. **Python's -m Switch**:
   - [Python's -m Switch](https://docs.python.org/3/using/cmdline.html#cmdoption-m) - Python documentation on the `-m` switch for running modules as scripts.

These resources should provide you with a deeper understanding of Python modules, packages, and the differences between running scripts and modules, as well as how to handle imports effectively.




Example: in *dbproject/dbapp/dbsetup/models.py*
    Change:
        from dbapp.dbsetup import database
    To:
        from . import database

