import sys



def get_options(args, prog_version='1.0', prog_usage='', misc_opts=None):

    return parser.parse_args(args)


def main(args):
    get_options(args)


if __name__ == "__main__":
    main(sys.argv[1:])