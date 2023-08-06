from .lboxd import *

parser = argparse.ArgumentParser(description='letterboxd args')
parser.add_argument('--user', '-u', dest='user', help='letterboxd.com user')
parser.add_argument('--reviews', '-r', dest='reviews', action="store_true", default=False, help='Gets reviews')
parser.add_argument('--testing', '-t', dest='testing', action='store_true', default=False, help='Testing flag - for development only')
parser.add_argument('--save-json', '-j', dest='json', action="store_true", default=False, help='Saves a JSON file of the reviews dictionary')
parser.add_argument('--save-html', '-w', dest='html', action="store_true", default=False, help='Saves an HTML document for easily viewing reviews')
parser.add_argument('--browser-open', '-b', dest='browserOpen', action="store_true", default=False, help='Opens saved HTML document in the browser')
parser.add_argument('--search', '-s', nargs='+', dest='search', default=())
args = parser.parse_args()



console = Console()

if __name__=='__main__':
    main()
