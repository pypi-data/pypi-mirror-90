import sys
import os

def project_root_path():
    """
    Returns the directory that contains the __main__ module
    """
    main_module = sys.modules['__main__']

    if not hasattr(main_module, '__file__'):
        raise Exception(f"The main module does not have the '__file__' attribute")

    return os.path.dirname(os.path.abspath(main_module.__file__))

def build_project_rooted_path(*args):
    """
    Creates a path using the components provided that is rooted at the 
    directory containing the __main__ module that (possibly indirectly)
    called this function
    """
    return os.path.join(
        project_root_path(),
        *args
    )