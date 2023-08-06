import argparse

from xnatpytools.utils import MyException, Logger
from xnatpytools.utils import XnatClient


LOG = None

CLIENT = None


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host')
    parser.add_argument('--user')
    parser.add_argument('--password')
    parser.add_argument('--source_project')
    parser.add_argument('--target_project')
    parser.add_argument('--test_run', type=int, default=1)
    parser.add_argument('--log_dir', default='.')
    parser.add_argument('--experiments', default=None)
    parser.add_argument('--experiments_file', default=None)
    args = parser.parse_args()
    return args


def show_intro():
    LOG.print("""
    === BULK SHARING ===
    Welcome to the bulk sharing tool of the XnatPyTools package!
    This tool allows you to share image experiments that are stored in XNAT from one project to another.
    """)


def get_client(args):
    global CLIENT
    if CLIENT is None:
        CLIENT = XnatClient(args.host, args.user, args.password, args.source_project)
    CLIENT.set_test_run(True if args.test_run == 1 else False)
    return CLIENT


def get_experiments(args):
    if args.experiments is not None and args.experiments != '':
        return [x.strip() for x in args.experiments.split(',')]
    with open(args.experiments_file, 'r') as f:
        experiments = []
        for experiment in f.readlines():
            experiments.append(experiment)
        return experiments


def share_experiments(experiments, args):
    client = get_client(args)
    client.share_experiments(experiments, args.target_project)


def run(args):
    show_intro()
    get_client(args)
    experiments = get_experiments(args)
    share_experiments(experiments, args)


def main():
    global LOG
    args = get_args()
    LOG = Logger(to_dir=args.log_dir)
    try:
        run(args)
    except MyException as e:
        LOG.print(e)


if __name__ == '__main__':
    main()
