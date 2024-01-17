import subprocess


def run(args, cwd=None):
    return subprocess.run(
        args=args,
        cwd=cwd,
        stdout=subprocess.PIPE,
    ).stdout.decode('utf-8')


def epm(args, cwd=None):
    return run(["epm"] + args, cwd=cwd)


def eget(args, cwd=None):
    return epm(["tool", "eget"] + args, cwd=cwd)

