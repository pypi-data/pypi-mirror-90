import os, sys
print('moofei', sys.argv)
print(os.getcwd())
#也可以将pkg作为一个Package执行：python -m pkg
from .._find import main
main()
exit(0)
