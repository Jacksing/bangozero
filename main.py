import os

if __name__ == '__main__':
    # os.environ.setdefault('PATH', '%PATHPY3%;')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

    from tests import start

    start()
