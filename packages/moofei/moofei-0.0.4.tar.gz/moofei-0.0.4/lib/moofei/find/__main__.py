import os, sys
print('moofei', sys.argv)
print(os.getcwd())
#Ҳ���Խ�pkg��Ϊһ��Packageִ�У�python -m pkg
from .._find import main
main()
exit(0)
