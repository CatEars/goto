import goto


def ident(elem):
    '''Return an identity function for elem.'''
    return lambda: elem


def test_empty_cond():
    '''Tests that empty cond is callable.'''
    res = goto.util.cond()
    assert res() is None


def test_single_value_cond():
    '''Test that a simple cond returns the right result.'''
    res = goto.util.cond(
        ('a', 'b')
    )()
    assert res == 'b'


def test_multiple_value_cond():
    '''Test that a simple cond returns the first truthy predicates associated value.'''
    res = goto.util.cond(
        ('a', 'b'),
        ('b', 'c')
    )()
    assert res == 'b'


def test_single_function_cond():
    '''Test cond with functions.'''

    res = goto.util.cond(
        (ident('a'), 'b')
    )()
    assert res == 'b'
    res = goto.util.cond(
        (ident('a'), ident('b'))
    )()
    assert res == 'b'
    res = goto.util.cond(
        ('a', ident('b'))
    )()
    assert res == 'b'


def test_multiple_function_cond():
    '''Test cond with multiple functions'''

    res = goto.util.cond(
        (ident('a'), ident('b')),
        (ident('b'), ident('c'))
    )()
    assert res == 'b'
    res = goto.util.cond(
        (ident(False), ident('b')),
        (ident('b'), ident('c'))
    )()
    assert res == 'c'

def test_with_arguments():
    '''Test with sending argument into functions of cond.'''

    def is_equal(elem):
        '''Return function that tests for equality.'''
        return lambda y: elem == y

    res = goto.util.cond(
        (is_equal('x'), 'y'),
        (is_equal('y'), 'z'),
        (is_equal('z'), 'x')
    )('z')
    assert res == 'x'
