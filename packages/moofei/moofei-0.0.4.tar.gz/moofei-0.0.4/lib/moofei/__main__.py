import os, sys
print('usage:')
for method in ('find', 'valid'):
    print(' '*4+' '.join([sys.executable, '-m', 'moofei.'+method, '-h']))


if len(sys.argv)>2:
    if sys.argv[1]==":find":
        from ._find import main
        main(cmd=":find")
exit(0)
