import sys
argv = sys.argv
argv = argv[argv.index("--") + 1:]

print(argv)

