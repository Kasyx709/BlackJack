from BlackJack.__main__ import main
import sys, multiprocessing

if __name__ == '__main__':
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    main()
