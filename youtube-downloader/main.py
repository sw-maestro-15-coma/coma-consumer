import recv, sys, os
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    host = os.environ.get('HOST')
    try:
        recv.consume(host)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

