import os
import sys

if __name__ == '__main__':
    # os.environ.setdefault('PATH', '%PATHPY3%;')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

    if len(sys.argv) > 1 and sys.argv[1][2:].startswith('entry='):
        arg_pair = sys.argv[1].split('=')
        try:
            if len(arg_pair) != 2 or not arg_pair[1].strip():
                raise ValueError
            exec('from %s import start' % arg_pair[1])
        except (ValueError, SyntaxError):
            print("Invalid launch configuration. '%s'" % sys.argv[1])
            sys.exit(0)
        except ImportError as ex:
            print(ex.message)
            sys.exit(0)
        exec('start()')
    else:
        pass
