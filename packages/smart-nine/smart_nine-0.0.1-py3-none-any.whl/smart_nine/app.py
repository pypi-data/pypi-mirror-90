import json
import argparse
import textwrap
import datetime
from . import smart_nine_gen as sn

def parse_bool(bool_str, parser, argument):
    """
    Parses boolean string to Bool
    """
    if isinstance(bool_str, bool):
       return bool_str
    if bool_str.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif bool_str.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        parser.print_help()
        raise argparse.ArgumentTypeError(f'Boolean value expected for ({argument}).')

def main():
    parser = argparse.ArgumentParser(
        description="smart-nine generates an instagram user's smart top 9 photograph collage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars='@')

    default_year = int(datetime.datetime.now().year)-1
    parser.add_argument('username', help='Instagram user(s) to generate a top 9', nargs='*')
    parser.add_argument('--login-user', '--login_user', '-u', default=None, help='Instagram scrapper login user')
    parser.add_argument('--login-pass', '--login_pass', '-p', default=None, help='Instagram scrapper login password')
    parser.add_argument('--year', '-y', type=int, default=default_year, help='Year for the top 9.')
    parser.add_argument('--timezone', '-t', type=str, default="America/Los_Angeles", help='Timezone of Instagram user(s)')
    parser.add_argument('--scrape', '-s', default=True, help='Data scrapping flag - set to False to work with local data.')
    args = parser.parse_args()

    if not args.username:
        parser.print_help()
        raise ValueError('Must provide username(s) OR a file containing a list of username(s) OR pass --followings-input')

    if (args.login_user is None and args.login_pass is None):
        parser.print_help()
        raise ValueError('Must provide login user AND password')

    if (args.login_user and args.login_pass is None) or (args.login_user is None and args.login_pass):
        parser.print_help()
        raise ValueError('Must provide login user AND password')

    if args.year < 2000:
        parser.print_help()
        raise ValueError('Year must be greater than 2000')

    args.scrape = parse_bool(args.scrape, parser, "--scrape, -s")

    smart = sn.SmartNineGen(usernames=args.username,
                            scrapper_user=args.login_user,
                            password=args.login_pass,
                            tz=args.timezone,
                            year=args.year)

    smart.smart_nine_gen(scrape_flag=args.scrape)

if __name__ == '__main__':
    print("Running main.")
    main()