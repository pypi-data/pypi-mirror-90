from os.path import abspath, dirname
from sys import path

path.append(dirname(dirname(abspath(__file__))))

from revli.cli import main

main()
