import re

from . import subst

# global lookups for defined functions and variables
__defined_functions = {}
__defined_variables = {}

def collect_information(exprs):
    """Initialize global lookups: defined functions and types."""
    global __defined_functions
    global __defined_variables
    __defined_functions = {}
    __defined_variables = {}

    for cmd in exprs:
        if not has_name(cmd):
            continue
        if get_name(cmd) == 'declare-const':
            if not len(cmd) == 3:
                continue
            assert is_leaf(cmd[1])
            __defined_variables[cmd[1]] = cmd[2]
        if get_name(cmd) == 'declare-fun':
            if not len(cmd) == 4:
                continue
            assert is_leaf(cmd[1])
            __defined_variables[cmd[1]] = cmd[3]
        if get_name(cmd) == 'define-fun':
            if not len(cmd) == 5:
                continue
            assert is_leaf(cmd[1])
            assert not is_leaf(cmd[2])
            if not is_leaf(cmd[3]):
                continue
            __defined_functions[cmd[1]] = lambda args, cmd=cmd: subst.subs_global(
                cmd[4],
                {cmd[2][i][0]: args[i] for i in range(len(args))}
            )

##### Generic utilities
def dfs(exprs):
    """DFS traversal of s-expressions in exprs."""
    visit = list(reversed(exprs))
    while visit:
        sexpr = visit.pop()
        if isinstance(sexpr, tuple):
            yield sexpr
            visit.extend(list(reversed(sexpr)))
        else:
            yield sexpr

def dfs_postorder(exprs):
    """Postorder DFS traversal of s-expressions in exprs."""
    visit = [(x, False) for x in exprs]
    while visit:
        sexpr, visited = visit.pop()
        if not isinstance(sexpr, tuple):
            continue

        if visited:
            yield sexpr
        else:
            visit.append((sexpr, True))
            visit.extend((x, False) for x in reversed(sexpr))


def node_count(node):
    return len(list(dfs(node)))

def filter_exprs(exprs, filter_func):
    """Filter s-expressions based on filter_func."""
    for expr in dfs(exprs):
        if filter_func(expr):
            yield expr

def has_type(node):
    """Checks whether :code:`node` was defined to have a certain type.
    Mostly applies to variables."""
    return is_leaf(node) and node in __defined_variables

def get_type(node):
    """Returns the type of :code:`node` if it was defined to have a certain type.
    Assumes :code:`has_type(node)`."""
    assert has_type(node)
    return __defined_variables[node]


def get_variables_with_type(var_type):
    """Returns all variables with the type :code:`var_type`."""
    return [
        v for v in __defined_variables
        if __defined_variables[v] == var_type
    ]

## Semantic testers

def is_leaf(node):
    """Checks whether the :code:`node` is a leaf node."""
    return not isinstance(node, tuple)

def has_name(node):
    """Checks whether the :code:`node` has a name,
    that is its first child is a leaf node."""
    return not is_leaf(node) and not node == () and is_leaf(node[0])

def get_name(node):
    """Gets the name of the :code:`node`,
    asserting that :code:`has_name(node)`."""
    assert has_name(node)
    return node[0]

def is_operator(node, name):
    return has_name(node) and get_name(node) == name

def is_indexed_operator(node, name, index_count = 1):
    if is_leaf(node) or len(node) < 2:
        return False
    if has_name(node) or not has_name(node[0]):
        return False
    if node[0][0] != '_' or node[0][1] != name:
        return False
    return len(node[0]) == index_count + 2


def is_nary(node):
    """Checks whether the :code:`node` is a n-ary operator."""
    if is_leaf(node) or not has_name(node):
        return False
    return get_name(node) in [
        '=>', 'and', 'or', 'xor', '=', 'distinct',
        '+', '-', '*', 'div', '/',
        '<=', '<', '>=', '>',
        'bvand', 'bvor', 'bvadd', 'bvmul', 'concat'
    ]

def is_boolean_constant(node):
    """Checks whether the :code:`node` is a Boolean constant."""
    return is_leaf(node) and node in ['false', 'true']

def is_arithmetic_constant(node):
    """Checks whether the :code:`node` is an arithmetic constant."""
    return is_leaf(node) and re.match('[0-9]+(\\.[0-9]*)?', node) is not None

def is_int_constant(node):
    """Checks whether the :code:`node` is an int constant."""
    return is_leaf(node) and re.match('^[0-9]+$', node) is not None

def is_real_constant(node):
    """Checks whether the :code:`node` is a real constant."""
    return is_leaf(node) and re.match('^[0-9]+(\\.[0-9]*)?$', node) is not None

def is_string_constant(node):
    """Checks whether the :code:`node` is a string constant."""
    return is_leaf(node) and re.match('^\"[^\"]*\"$', node) is not None

def is_bitvector_constant(node):
    if is_leaf(node):
        if node.startswith('#b'):
            return True
        if node.startswith('#x'):
            return True
        return False
    if len(node) != 3:
        return False
    if not has_name(node) or get_name(node) != '_':
        return False
    return node[1].startswith('bv')

def is_constant(node):
    return is_boolean_constant(node) or is_arithmetic_constant(node) or is_int_constant(node) or is_real_constant(node) or is_string_constant(node) or is_bitvector_constant(node)


def is_defined_function(node):
    """Checks whether :code:`node` is a defined function."""
    if is_leaf(node):
        return node in __defined_functions
    return has_name(node) and get_name(node) in __defined_functions

def get_defined_function(node):
    """Returns the defined function :code:`node`, instantiated with the arguments of :code:`node` if necessary.
    Assumes :code:`__is_defined_functions(node)`."""
    assert is_defined_function(node)
    if is_leaf(node):
        return __defined_functions[node]([])
    return __defined_functions[get_name(node)](node[1:])

def get_constants(const_type):
    """Returns a list of constants for the given type."""
    if const_type == 'Bool':
        return ['false', 'true']
    if const_type == 'Int':
        return ['0', '1']
    if const_type == 'Real':
        return ['0.0', '1.0']
    if is_bitvector_type(const_type):
        return [['_', c, const_type[2]] for c in ['bv0', 'bv1']]
    if is_set_type(const_type):
        return [['as', 'emptyset', const_type]] + [
            ['singleton', c] for c in get_constants(const_type[1])
        ]
    return []

def get_return_type(node):
    """Tries to figure out the return type of the given node.
    Returns :code:`None` if it can not be inferred."""
    if has_type(node):
        return get_type(node)
    if is_boolean_constant(node):
        return 'Bool'
    if is_bitvector_constant(node):
        return ['_', 'BitVec', str(get_bitvector_width(node))]
    if is_int_constant(node):
        return 'Int'
    if is_real_constant(node):
        return 'Real'
    bvwidth = get_bitvector_width(node)
    if bvwidth != -1:
        return ['_', 'BitVec', str(bvwidth)]
    if has_name(node):
        if is_operator(node, 'ite'):
            return get_return_type(node[1])
        # stuff that returns Bool
        if get_name(node) in [
                # core theory
                'not', '=>', 'and', 'or', 'xor', '=', 'distinct',
                # bv theory
                'bvult',
                # fp theory
                'fp.leq', 'fp.lt', 'fp.geq', 'fp.gt', 'fp.eq',
                'fp.isNormal', 'fp.isSubnormal', 'fp.isZero',
                'fp.isInfinite', 'fp.isNaN',
                'fp.isNegative', 'fp.isPositive',
                # int / real theory
                '<=', '<', '>>', '>', 'is_int',
                # sets theory
                'member', 'subset',
                # string theory
                'str.<', 'str.in_re', 'str.<=',
                'str.prefixof', 'str.suffixof', 'str.contains',
                'str.is_digit',
        ]:
            return 'Bool'
        # int theory
        if get_name(node) == '_' and len(node) == 3 and node[1] == 'divisible':
            return 'Bool'
        # stuff that returns Int
        if get_name(node) in [
                'div', 'mod', 'abs', 'to_int',
                # string theory
                'str.len', 'str.indexof', 'str.to_code', 'str.to_int',
                # sets theory
                'card'
        ]:
            return 'Int'
        # stuff that returns Real
        if get_name(node) in ['/', 'to_real', 'fp.to_real']:
            return 'Real'
        if get_name(node) in ['+', '-', '*']:
            if any(map(lambda n: get_return_type(n) == 'Real', node[1:])):
                return 'Real'
            else:
                return 'Int'
    return None


def is_bitvector_type(node):
    if is_leaf(node) or len(node) != 3:
        return False
    if not has_name(node) or get_name(node) != '_':
        return False
    return node[1] == 'BitVec'

def is_set_type(node):
    if is_leaf(node) or len(node) != 2:
        return False
    if not has_name(node) or get_name(node) != 'Set':
        return False
    return True

def get_bitvector_width(node):
    if is_bitvector_constant(node):
        if is_leaf(node):
            if node.startswith('#b'):
                return len(node[2:])
            if node.startswith('#x'):
                return len(node[2:]) * 4
        return int(node[2])
    if has_type(node):
        assert is_bitvector_type(get_type(node))
        return int(get_type(node)[2])
    if has_name(node):
        if get_name(node) in [
                'bvnot', 'bvand', 'bvor',
                'bvneg', 'bvadd', 'bvmul', 'bvudiv', 'bvurem',
                'bvshl', 'bvshr',
                'bvnand', 'bvnor', 'bvxor', 'bvsub', 'bvsdiv',
                'bvsrem', 'bvsmod', 'bvashr'
        ]:
            return get_bitvector_width(node[1])
        if get_name(node) == 'concat':
            assert len(node) == 3
            return get_bitvector_width(node[1]) + get_bitvector_width(node[2])
        if get_name(node) == 'bvcomp':
            return 1
        if is_indexed_operator(node, 'extend'):
            return int(node[0][2]) + get_bitvector_width(node[1])
        if is_indexed_operator(node, 'extract', 2):
            return int(node[0][2]) - int(node[0][3]) + 1
        if is_indexed_operator(node, 'repeat'):
            return int(node[0][2]) * get_bitvector_width(node[1])
        if is_indexed_operator(node, 'rotate'):
            return get_bitvector_width(node[1])
    return -1
