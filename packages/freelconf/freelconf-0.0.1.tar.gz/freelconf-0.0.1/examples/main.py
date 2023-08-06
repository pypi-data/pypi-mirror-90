from freelconf.parser import ConfParser
import sys

if __name__ == "__main__":
    ConfParser.compile([sys.argv[1]], sys.argv[2], sys.argv[3])