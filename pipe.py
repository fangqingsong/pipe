import os
import sys

def main(cmd):
    cmds = [cmd.strip() for cmd in cmd.split("|")]
    run_cmds(cmds, ())


def run_cmds(cmds, left_pipe):
    cur_cmd = cmds[0]
    other_cmds = cmds[1:]
    pipe_fds = ()
    if other_cmds:
        pipe_fds = os.pipe()
    pid = os.fork()
    if pid < 0:
        print "fork process failed"
        return
    if pid == 0:
        run_cmd(cur_cmd, left_pipe, pipe_fds)
    elif other_cmds:
        if left_pipe:
            os.close(left_pipe[0])
            os.close(left_pipe[1])
        run_cmds(other_cmds, pipe_fds)


def run_cmd(cmd, left_pipe, right_pipe):
    print cmd, os.getpid(), os.getppid()
    if left_pipe:
        os.dup2(left_pipe[0], sys.stdin.fileno())
        os.close(left_pipe[0])
        os.close(left_pipe[1])
    if right_pipe:
        os.dup2(right_pipe[1], sys.stdout.fileno())
        os.close(right_pipe[0])
        os.close(right_pipe[1])
    args = [arg.strip() for arg in cmd.split()]
    args = [arg for arg in args if arg]
    try:
        os.execvp(args[0], args)
    except OSError as ex:
        print "exec error:", ex


if __name__ == '__main__':
    main(sys.argv[1])
