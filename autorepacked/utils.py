import subprocess


def run(args, cwd=None):
    return subprocess.run(
        args=args,
        cwd=cwd,
        stdout=subprocess.PIPE,
    ).stdout.decode('utf-8')
