import copy
import functools
import inspect

import astroid


def print_statements_transform(node):
    node_str = node.as_string().rstrip()
    if '\n' in node_str:
        return node
    else:
        return astroid.parse(f'print("{node_str}"); {node_str}', apply_transforms=False)


@functools.lru_cache(maxsize=None)
def _register_once(node_type, transformer, predicate=None):
    astroid.MANAGER.register_transform(node_type, transformer, predicate=predicate)


def annotate_function(func):
    calling_frame = inspect.stack()[1].frame
    source_lines = inspect.getsource(func).splitlines()[1:]  # Skip decorator line
    for node_type in astroid.ALL_NODE_CLASSES:
        if node_type.is_statement:
            _register_once(node_type, print_statements_transform)

    root = astroid.parse('\n'.join(source_lines))
    code = compile(root.as_string(), func.__code__.co_filename, 'exec')
    namespace = copy.copy(calling_frame.f_globals)
    namespace.update(copy.copy(calling_frame.f_locals))
    exec(code, namespace)

    @functools.wraps(func)
    def _wrapped(*args, **kwargs):
        return namespace[func.__name__](*args, **kwargs)

    return _wrapped


@annotate_function
def test_func():
    a = 1 + 1
    return a


if __name__ == '__main__':
    print(test_func())
