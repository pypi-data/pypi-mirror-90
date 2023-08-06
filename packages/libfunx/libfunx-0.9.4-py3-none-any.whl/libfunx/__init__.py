"""LIBrary of utility FUNCtionS for catpdf minmon swapdf toc2md wmtile"""

__version__ = "0.9.4"

__all__ = ['ask', 'bad_char', 'char_set', 'chars', 'difs', 'drop', 'dupl',
	'fibonacci', 'find', 'find_in', 'find_max', 'find_min', 'find_not_in', 'find_dup', 'frange', 'freq', 
	'func_fixed', 'func_zero', 'get_path_files', 'get_paths', 'get_source', 
	'get_target', 'integral', 'is_date_time', 'leap_year', 'min_qua_max', 
	'month_days', 'moving_means', 'no_comment', 'no_tag', 'package_file', 'replace', 'rfind', 
	'rfind_in', 'rfind_max', 'rfind_min', 'rfind_not_in', 'shell', 'split', 'sql_quote', 'sql_unquote', 
	'str_exception', 'sums', 'syntax_error', 'take', 'test_type', 'try_func', 
	'uniq', 'year_days']

# imports

from fnmatch import fnmatch
from glob import glob
from os import chdir, listdir, walk
from os.path import split as splitpath, join as joinpath, abspath, expanduser, isfile, isdir, islink, exists
from statistics import quantiles
from subprocess import run, PIPE
from sys import argv, exit, stdin, stdout, stderr

# string functions

def take(string, allowed, default=''):
    """take allowed chars from string and replace not allowed chars by default
>>> take("take allowed", "aeiou")
'aeaoe'
>>> take("take allowed", "aeiou", "?")
'?a?e?a??o?e?'"""
    return ''.join(char if char in allowed else default for char in string)

def drop(string, forbidden, default=''):
    """drop forbidden chars from string and replace them by default
>>> drop("drop forbidden", "aeiou")
'drp frbddn'
>>> drop("drop forbidden", "aeiou", "->")
'dr->p f->rb->dd->n'
    """
    return ''.join(default if char in forbidden else char for char in string)

def split(string, sep=None):
    """return [] if not string else string.split(sep)
>>> split("") == split("", None) == [] == "".split()
True
>>> split("", ",") == [] != "".split(",") == [""]
True
>>> split("a", ",") == ["a"] == "a".split(",")
True
>>> split("a,b", ",") == ["a", "b"] == "a,b".split(",")
True"""
    return [] if not string else string.split(sep)

def replace(string, *oldsnews):
    """replace(string, old0, new0, old1, new1, ...) ==
    string.replace(old0, new0).replace(old1, new1)...
>>> replace("abcdefghijklmnopqrstuvwxyz", "a", "A", "e", "E", "i", "I", "o", "O", "u", "U")
'AbcdEfghIjklmnOpqrstUvwxyz'
>>> replace("abcdefghijklmnopqrstuvwxyz", *["a", "A", "e", "E", "i", "I", "o", "O", "u", "U"])
'AbcdEfghIjklmnOpqrstUvwxyz'
>>> replace("abcdefghijklmnopqrstuvwxyz", *"aAeEiIoOuU")
'AbcdEfghIjklmnOpqrstUvwxyz'"""
    for j in range(0, len(oldsnews), 2):
        string = string.replace(oldsnews[j], oldsnews[j+1])
    return string

def no_tag(string, left="<", right=">"):
    """remove tags from string
>>> no_tag('abc<def>ghi</def>jkl')
'abcghijkl'
>>> no_tag('abc{def}ghi{/def}jkl', "{", "}")
'abcghijkl'"""
    result = ""; tag = False
    for char in string:
        if char == left:
            tag = True
        if not tag:
            result += char
        if char == right:
            tag = False
    if tag:
        raise SyntaxError("unmatched {left!r} tag in {string!r}")
    else:
        return result

def no_comment(string):
    """remove #-comment from string
>>> no_comment("echo 'pound: #' # a quoted '#' doesn't start the comment")
"echo 'pound: #'"
"""
    quote = 0
    for jchar, char in enumerate(string):
        if char == "'" and quote != 2:
            quote = 1 - quote
        elif char == '"' and quote != 1:
            quote = 2 - quote
        elif char =="#" and quote == 0:
            return string[:jchar].strip()
    if quote:
        which = ["single", "double"][quote - 1]
        raise SyntaxError(f"unmatched {which} quotation mark in {string!r}")
    else:
        return string.strip()

def chars(which=""):
    """return a string defined by which
which is a comma-separated list of zero or more nintervals
each interval is:
    a 1-char str or ...
    ... a 3-chars str == (first char + "-" + last char)
>>> chars()
''
>>> chars("")
''
>>> chars("a-z")
'abcdefghijklmnopqrstuvwxyz'
>>> chars("z-a")
'zyxwvutsrqponmlkjihgfedcba'
>>> chars("a-z,A-Z,_")
'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
>>> chars("a-z,A:Z,_")
SyntaxError: in 'a-z,A(:?)Z,_'
"""
    test_type(which, (str,))
    status = 0; result = ""; first, last = "", ""
    for jchar, char in enumerate(which):
        # print('-->', jchar, char, status)
        if status < 2:
            if char not in "-,":
                first = char
                status = 2
            else:
                syntax_error(which, jchar)
        elif status == 2:
            if char == "-":
                status = 3
            elif char == ",":
                result += first
                first = ""
                status = 1
            else:
                syntax_error(which, jchar)
        elif status == 3:
            if char not in "-,":
                last = char
                status = 4
            else:
                syntax_error(which, jchar)
        else: # status == 4
            if char == ",":
                stop, step = (ord(last) + 1, 1) if first <= last else (ord(last) - 1, -1)
                result += ''.join(chr(j) for j in range(ord(first), stop, step))
                first, last = "", ""
                status = 1
            else:
                syntax_error(which, jchar)
    if last:
        stop, step = (ord(last) + 1, 1) if first <= last else (ord(last) - 1, -1)
        result += ''.join(chr(j) for j in range(ord(first), stop, step))
    elif first:
        result += first
    if status not in {0, 2, 4}:
        syntax_error(which, jchar)
    return result

def char_set(which=""):
    """return a frozenset of chars defined by which (see chars()):
>>> char_set("a-z") == frozenset(chars("a-z"))
True
"""
    return frozenset(chars(which))

def sql_quote(string:str="") -> str:
    """return standard SQL quoting of string, examples:

>>> sql_quote("'")
"''''"
>>> sql_quote("isn't it?")
"'isn''t it?'"

example of wrong argument:

>>> sql_quote(None)
TypeError: NoneType (should be str)
"""
    test_type(string, (str,))
    return "'" + string.replace("'", "''") + "'"

def sql_unquote(string:str="''") -> str:
    """return standard SQL unquoting of string, examples:

>>> sql_unquote("''''")
"'"
>>> sql_unquote("'isn''t it?'")
"isn't it?"
>>> sql_unquote(sql_quote("isn't it?")) == "isn't it?"
True

examples of wrong arguments:

>>> sql_unquote(None)
TypeError: NoneType (should be str)
>>> sql_unquote("isn't it?")
SyntaxError: in "(i?)sn't it?"
>>> sql_unquote("'isn't it?")
SyntaxError: in "'isn'(t?) it?"
>>> sql_unquote("'isn''t it?")
SyntaxError: in "'isn''t it(??)"
"""
    test_type(string, (str,))
    status = 0; result = ""
    for jchar, char in enumerate(string):
        if status == 0:
            if char != "'":
                syntax_error(string, jchar)
            status = 1
        elif status == 1:
            if char == "'":
                status = 2
            else:
                result += char
        else: # status == 2
            if char != "'":
                syntax_error(string, jchar)
            result += "'"
            status = 1
    if status != 2:
        syntax_error(string, jchar)
    return result

# shell functions

def ask(question, answers="yn"):
    "return answer to terminal question"
    answers = {char.lower() for char in answers}
    while True:
        answer = input(question).strip().lower()
        if answer in answers:
            return answer

def shell(command, out="r", err="n", echo=False):
    """
if echo: print prompt and command)
result <-- command
out controls result.stdout:
    if out="n": doN't pipe, send directly to sys.stdout, return []
    if out="r": pipe and Return as a list of rstripped strings
    if out="w": pipe, Write into stdout and return as a list of rstripped strings
err controls result.stderr:
    if err="n": doN't pipe, send directly to sys.stderr
    if err="w": pipe and on error Write into sys.stderr
    if err="e": pipe and on error raise OSError(error)
    if err="x": pipe and on error eXit(error)
return out_lines
>>> shell('''echo "isn't it?"''')
["isn't it?"]
>>> shell('qqqq', err='e')
OSError: /bin/sh: 1: qqqq: not found
"""
    # check arguments
    out = out.strip(); assert out in set("nrw")
    err = err.strip(); assert err in set("nwex")
    if echo:
        print(abspath("."), "-->", command)
    command = no_comment(command)
    if command == "cd":
        command = "cd ~"
        
    # execute command
    output, error = "", ""
    if command.startswith("cd "):
        is_cd = True
        cd_arg = command[3:].strip()
        globs = glob(abspath(expanduser(cd_arg)))
        # print(f"{globs = }")
        if not globs:
            error = f"cd: {cd_arg}: No such file or directory"
        elif len(globs) > 1:
            error = f"cd: Too many arguments"
        else:
            try:
                chdir(globs[0])
            except Exception as exception:
                rexc = repr(exception)
                error = "cd: " + eval(rexc[rexc.find("'"):rexc.rfind("'")+1])
    else:
        is_cd = False
        result = run(command, shell=True, text=True,
            stdout=None if out == "n" else PIPE,
            stderr=None if err == "n" else PIPE)
        output, error = result.stdout, result.stderr
        
    # process output
    if out == "w":
        print(output, file=stdout)

    # process error
    if error:
        if err == "w" or is_cd and err == "n":
            print(error, file=stderr)
        elif err == "e":
            raise OSError(error)
        elif err == "x":
            exit(error)

    # return output as a list of rstripped strings
    out_lines = [line.rstrip() for line in output.split("\n")] if output else []
    while out_lines and not out_lines[-1]:
        out_lines.pop() # drop tailing empty lines
    return out_lines

# sequence functions

def find(xx, y):
    """find min j such that xx[j] == y, -1 if not found
>>> find("abracadabra", "r")
2
>>> find("abracadabra", "z")
-1"""
    for j, xj in enumerate(xx):
        if xj == y:
            return j
    else:
        return -1

def rfind(xx, y):
    """find max j such that xx[j] == y, -1 if not found
>>> rfind("abracadabra", "r")
9
>>> rfind("abracadabra", "z")
-1
    """
    for j in range(len(xx) - 1, -1, -1):
        if xx[j] == y:
            return j
    else:
        return -1

def find_dup(xx):
    """find min j such that xx[j] == xx[i] for some i < j, -1 if not found
>>> find_dup("abracadabra")
3
>>> find_dup("0123456789")
-1
"""
    xset = set()
    for j, xj in enumerate(xx):
        if xj in xset:
            return j
        xset.add(xj)
    else:
        return -1

def find_max(xx):
    """find min j such that xx[j] == max(xx), -1 if not xx
>>> find_max("abracadabra")
2
>>> find_max("")
-1
"""
    if not xx:
        return -1
    for j, xj in enumerate(xx):
        if j == 0 or xj > xmin:
            jmin, xmin = j, xj
    return jmin

def rfind_max(xx):
    """find max j such that xx[j] == max(xx), -1 if not xx
>>> rfind_max("abracadabra")
9
>>> rfind_max("")
-1
"""
    if not xx:
        return -1
    for j, xj in enumerate(xx):
        if j == 0 or xj >= xmin:
            jmin, xmin = j, xj
    return jmin

def find_min(xx):
    """find min j such that xx[j] == min(xx), -1 if not xx
>>> find_min("abracadabra")
0
>>> find_min("")
-1
"""
    if not xx:
        return -1
    for j, xj in enumerate(xx):
        if j == 0 or xj < xmin:
            jmin, xmin = j, xj
    return jmin

def rfind_min(xx):
    """find max j such that xx[j] == min(xx), -1 if not xx
>>> rfind_min("abracadabra")
10
>>> rfind_min("")
-1
"""
    if not xx:
        return -1
    for j, xj in enumerate(xx):
        if j == 0 or xj <= xmin:
            jmin, xmin = j, xj
    return jmin

def find_in(xx, yy):
    """find min j such that xx[j] in yy, -1 if not found
>>> find_in("abracadabra", "pqr")
2
>>> find_in("abracadabra", "xyz")
-1
    """
    for j, xj in enumerate(xx):
        if xj in yy:
            return j
    else:
        return -1

def find_not_in(xx, yy):
    """find min j such that xx[j] not in yy, -1 if not found
>>> find_not_in("abracadabra", "pqr")
0
>>> find_not_in("abracadabra", "bra")
4
>>> find_not_in("abracadabra", "xyz")
0
>>> find_not_in("abracadabra", "abcdr")
-1
    """
    for j, xj in enumerate(xx):
        if xj not in yy:
            return j
    else:
        return -1

def rfind_in(xx, yy):
    """find last j such that xx[j] in yy, -1 if not found
>>> rfind_in("abracadabra", "pqr")
9
>>> rfind_in("abracadabra", "xyz")
-1
    """
    for j in range(len(xx) - 1, -1, -1):
        if xx[j] in yy:
            return j
    else:
        return -1

def rfind_not_in(xx, yy):
    """find last j such that xx[j] not in yy, -1 if not found
>>> rfind_not_in("abracadabra", "pqr")
10
>>> rfind_not_in("abracadabra", "bra")
6
>>> rfind_not_in("abracadabra", "xyz")
10
>>> rfind_not_in("abracadabra", "abcdr")
-1
    """
    for j in range(len(xx) - 1, -1, -1):
        if xx[j] not in yy:
            return j
    else:
        return -1

# file functions

def get_paths(path, recursive=False):
    path = abspath(expanduser(path))
    if recursive:
        for root, dirs, files in walk(path):
            yield joinpath(path, root)
    else:
        for dir in listdir(path):
            path_dir = joinpath(path, dir)
            if isdir(path_dir):
                yield path_dir

def get_path_files(path_pattern, recursive=False):
    path, pattern = splitpath(abspath(expanduser(path_pattern)))
    if recursive:
        for root, dirs, files in walk(path):
            for file in files:
                if fnmatch(file, pattern):
                    yield joinpath(path, root, file)
    else:
        for file in listdir(path):
            path_file = joinpath(path, file)
            if isfile(path_file) and fnmatch(file, pattern):
                yield path_file

def get_source(source, ext=""):
    "check source file and return it as absolute path"
    if not isinstance(source, str):
        exit(f"ERROR: source not given")
    source = abspath(expanduser(source))
    if not source.endswith(ext):
        exit(f"ERROR: source {source!r} does not end with {ext!r}")
    elif not exists(source):
        exit(f"ERROR: source {source!r} does not exist")
    elif not isfile(source):
        exit(f"ERROR: source {source!r} exists but is not a file")
    else:
        return source
        
def get_target(target, ext="", yes=False, no=False):
    "check target file and return it as absolute path"
    if not isinstance(target, str):
        exit(f"ERROR: target not given")
    if yes and no:
        exit("ERROR: you can't give both yes and no arguments")
    target = abspath(expanduser(target))
    if not target.endswith(ext):
        exit(f"ERROR: target {target!r} doesn't end with {ext!r}")
    elif exists(target):
        if not isfile(target):
            exit(f"ERROR: target {target!r} exists and is not a file")
        elif no or not yes and ask(f"target file {target!r} exists, overwrite? (y/n) --> ") == "n":
            exit(f"target file {target!r} exists, not overwritten")
    return target

def package_file(name):
    "get absolute path of file in package"
    return joinpath(splitpath(__file__)[0], name)

# lists & dicts functions

def freq(xx):
    """return dict of frequencies of x in xx
>>> freq('abracadabra')
{'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}"""
    xn = {}
    for x in xx:
        try:
            xn[x] += 1
        except KeyError:
            xn[x] = 1
    return xn

def uniq(xx):
    """return list (with no duplicates) of x in xx
>>> uniq('abracadabra')
['a', 'b', 'r', 'c', 'd']"""
    yy = set()
    uu = []
    for x in xx:
        if x not in yy:
            uu.append(x)
            yy.add(x)
    return uu

def dupl(xx):
    """return list (with no duplicates) of duplicated x in xx
>>> dupl('abracadabra')
['a', 'b', 'r']"""
    xn = freq(xx)
    return(uniq(x for x in xx if xn[x] > 1))

def fibonacci(n):
    """
bidirectional Fibonacci numbers, f(n) == f(n-2) + f(n-1) for any integer n
>>> for n in range(-9, 10): print(n, fibonacci(n))
-9 34
-8 -21
-7 13
-6 -8
-5 5
-4 -3
-3 2
-2 -1
-1 1
0 0
1 1
2 1
3 2
4 3
5 5
6 8
7 13
8 21
9 34
>>> fibonacci(100) / fibonacci(99) # phi = golden ratio
1.618033988749895
>>> fibonacci(99) / fibonacci(100) # psi = inverse of golden ratio
0.6180339887498949
"""
    if n == 0:
        return 0
    elif n > 0:
        p, q = 0, 1
        for j in range(n - 1):
            p, q = q, p + q
        return q
    else: # n < 0:
        p, q = 0, 1
        for j in range(-n):
            p, q = q - p, p
        return p

# statistical functions

def difs(xx):
    """finite differences yy: yy[0] = xx[0], yy[i] = xx[i] - xx[i-1]
>>> xx = list(range(10, 20))
>>> difs(xx)
[10, 1, 1, 1, 1, 1, 1, 1, 1, 1]
>>> xx == difs(sums(xx)) == sums(difs(xx))
True
"""
    dd = []; xi = 0
    for xj in xx:
        dd.append(xj - xi)
        xi = xj
    return dd
    
def sums(xx):
    """progressive sums yy: yy[0] == xx[0], yy[i] = yy[i-1] + xx[i]
>>> xx = list(range(10, 20))
>>> sums(xx)
[10, 21, 33, 46, 60, 75, 91, 108, 126, 145]
>>> xx == difs(sums(xx)) == sums(difs(xx))
True
"""
    ss = []; sj = 0
    for xj in xx:
        sj += xj
        ss.append(sj)
    return ss

def moving_means(xx, n):
    """return [yy[j] = sum(xx[j+1-n:j+1]) / n]
>>> moving_means(list(range(10)), 7)
[0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]
>>> moving_means(list(range(10)), 3)
[0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
"""
    return [sum(xx[max(0, j + 1 - n): j + 1]) / min(n, j + 1) for j in range(len(xx))]

def min_qua_max(xx, n, method="inclusive"):
    """
return [min(xx)] + quantiles(xx, n=n, method="inclusive") + [max(xx)]
>>> from random import seed, random
>>> seed(314159)
>>> xx = [random() for j in range(100000)] # 100000 random floats between 0.0 and 1.0
>>> min_qua_max(xx, 4) # [min(xx), 1st quartile, 2nd quartile == median, 3rd quartile, max(xx)]
[3.2640170710696026e-06, 0.24956912051054536, 0.5016910963353665, 0.750802842987178, 0.9999873492923799]
>>> min_qua_max(xx, 10) # deciles
[3.2640170710696026e-06, 0.10118755218419968, 0.20026893496215079, 0.29966323718726284, 0.40097187287064084, 0.5016910963353665, 0.6015193723293496, 0.70106377365372, 0.8006989612789306, 0.8999854251451112, 0.9999873492923799]"""
    return [min(xx)] + quantiles(xx, n=n, method=method) + [max(xx)]

# float functions

def frange(start, stop, nint, first=True, last=False):
    """float range
>>> list(frange(0, 1, 7, last=True))
[0.0, 0.14285714285714285, 0.2857142857142857, 0.42857142857142855, 0.5714285714285714, 0.7142857142857142, 0.8571428571428571, 1.0]
>>> list(frange(1, 0, 7, last=True))
[1.0, 0.8571428571428572, 0.7142857142857143, 0.5714285714285714, 0.4285714285714286, 0.2857142857142858, 0.1428571428571429, 0.0]
"""
    if first:
        yield float(start)
    delta = (stop - start) / nint
    for j in range(1, nint):
        yield start + j * delta
    if last:
        yield float(stop)
        
def integral(f, xa, xz, maxerr=1e-12):
    """
definite integral of f(x) between xa and xz, by Simpson's rule
>>> integral(lambda x: x * x, 0.0, 1.0) # == 1 / 3
0.3333333333333333
"""
    s0 = None
    for p in range(4, 25):
        n = 2 ** p
        h = (xz - xa) / n
        s = (h / 3.0) * (f(xa) +
             4.0 * sum(f(xa + j * h) for j in range(1, n, 2)) +
             2.0 * sum(f(xa + j * h) for j in range(2, n - 1, 2)) + f(xz))
        if p == 24 or s0 is not None and abs(s - s0) <= maxerr:
            return s
        s0 = s

def func_zero(f, xa, xz):
    """
return x between xa and xz such that f(x) == 0.0, by regula falsi
must be xa < xz and f(xa) * f(xz) < 0.0 and one zero only in [xa, xz] interval
>>> func_zero(lambda x: x * x - x - 1.0, 0.0, 2.0) # phi = golden ratio
1.618033988749895
>>> func_zero(lambda x: x * x + x - 1.0, 0.0, 2.0) # psi = 1 / golden ratio
0.6180339887498948
"""
    assert xa < xz
    xa, xz = float(xa), float(xz)
    ya, yz = f(xa), f(xz)
    assert ya * yz < 0.0
    while True:
        xh = xa - ya * (xa - xz) / (ya - yz)
        yh = f(xh)
        if ya * yh > 0.0:
            if xa == xh:
                return xh
            xa, ya = xh, yh
        else:
            if xz == xh:
                return xh
            xz, yz = xh, yh

def func_fixed(f, x0=1.0):
    """
return x (starting from x0) such that x == f(x)
>>> func_fixed(lambda x: 1.0 / x + 1.0) # phi = golden ratio
1.618033988749895
>>> func_fixed(lambda x: 1.0 / x - 1.0) # psi = 1 / golden ratio
ZeroDivisionError: float division by zero
"""
    while True:
        x = f(x0)
        if x == x0:
            return x
        x0 = x
       
# time functions

def leap_year(Y):
    """
is Y a leap year? (proleptic gregorian calendar)
>>> [y for y in range(1000, 3001, 100) if leap_year(y)]
[1200, 1600, 2000, 2400, 2800]
>>> [y for y in range(1980, 2021) if leap_year(y)]
[1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020]
"""
    return Y % 4 == 0 and (Y % 100 != 0 or Y % 400 == 0)

def year_days(Y):
    """
number of days in year Y (proleptic gregorian calendar)
"""
    return 365 + leap_year(Y)

def month_days(Y, m):
    """
number of days in month m of year Y (proleptic gregorian calendar)
"""
    return [31, 28 + leap_year(Y), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]

def is_date_time(Y, m, d, H=0, M=0, S=0, Ymin=0, Ymax=9999):
    """
is date (and time) correct?
"""
    return (Ymin <= Y <= Ymax and 1 <= m <= 12 and 1 <= d <= month_days(Y, m) and
            0 <= min(H, M, S) <= max(H, M, S) <= 59)

def easter_month_day(Y):
    """return Easter date of year Y as (month, day)
>>> for Y in range(2020, 2030): print((Y,) + easter_month_day(Y))
(2020, 4, 12)
(2021, 4, 4)
(2022, 4, 17)
(2023, 4, 9)
(2024, 3, 31)
(2025, 4, 20)
(2026, 4, 5)
(2027, 3, 28)
(2028, 4, 16)
(2029, 4, 1)
"""
    a = Y % 19
    b = Y // 100
    c = Y % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    return f // 31, f % 31 + 1

# various functions

def try_func(func, args, on_error=None):
    """try: return func(*args); except: return on_error
>>> from math import sqrt
>>> try_func(sqrt, (4.0,), '???')
2.0
>>> try_func(sqrt, (-4.0,), '???')
'???'"""
    try:
        return func(*args)
    except:
        return on_error

def test_type(x, types):
    """
>>> test_type(314, (int, str))
>>> test_type(3.14, (int, str))
TypeError: float (should be int or str)
"""
    if not isinstance(x, types):
        raise TypeError(f"{type(x).__name__} (should be {' or '.join(type.__name__ for type in types)})")

def bad_char(string:str, jchar:int) -> str:
    """return string with bad char surrounded by "(" and "?)"
>>> bad_char("", 0)
'(?)'
>>> for j in range(-2, 7): print("%2d -> %r" % (j, bad_char("abcde", j)))
-2 -> '(a?)bcde'
-1 -> '(a?)bcde'
 0 -> '(a?)bcde'
 1 -> 'a(b?)cde'
 2 -> 'ab(c?)de'
 3 -> 'abc(d?)e'
 4 -> 'abcd(e?)'
 5 -> 'abcd(e?)'
 6 -> 'abcd(e?)'
"""
    if string:
        jchar = max(0, min(jchar, len(string) - 1))
        return f"{string[:jchar]}({string[jchar]}?){string[jchar+1:]}"
    else:
        return '(?)'

def syntax_error(string:str, j:int=None):
    """
>>> syntax_error("abcdefgh", 3)
SyntaxError: in 'abc(d?)efgh'
"""
    if not string:
        raise ValueError(f"syntax error in '' (null string not allowed)")
    else:
        j = max(0, min(len(string) - 1, j))
        raise SyntaxError(f"in {bad_char(string, j)!r}")

def str_exception(exception):
    """message from exception:
>>> str_exception(ZeroDivisionError('division by zero'))
'ZeroDivisionError: division by zero'
    """
    name, error = repr(exception).split("(", 1)
    return f"{name}: {eval(error[:-1])}"




