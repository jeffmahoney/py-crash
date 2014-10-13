#!/usr/bin/env python
# vim: sw=4 ts=4 et si:

import gdb

from crashcommand import CrashCommand
import argparse
from crash.cache.syms import get_value

charp = gdb.lookup_type('char').pointer()

class FilesCommand(CrashCommand):
    """
NAME
  files - open files

SYNOPSIS
  files [-d dentry] | [-R reference] [pid | taskp] ... 

DESCRIPTION
  This command displays information about open files of a context.
  It prints the context's current root directory and current working
  directory, and then for each open file descriptor it prints a pointer
  to its file struct, a pointer to its dentry struct, a pointer to the
  inode, the file type, and the pathname.  If no arguments are entered,
  the current context is used.  The -R option, typically invoked from
  "foreach files", searches for references to a supplied number, address,
  or filename argument, and prints only the essential information leading
  up to and including the reference.  The -d option is not context
  specific, and only shows the data requested.

     -d dentry  given a hexadecimal dentry address, display its inode,
                super block, file type, and full pathname.
  -R reference  search for references to this file descriptor number,
                filename, or dentry, inode, or file structure address.
           pid  a process PID.
         taskp  a hexadecimal task_struct pointer.

EXAMPLES
  Display the open files of the current context:

    crash> files
    PID: 720    TASK: c67f2000  CPU: 1   COMMAND: "innd"
    ROOT: /    CWD: /var/spool/news/articles
     FD    FILE     DENTRY    INODE    TYPE  PATH
      0  c6b9c740  c7cc45a0  c7c939e0  CHR   /dev/null
      1  c6b9c800  c537bb20  c54d0000  REG   /var/log/news/news
      2  c6df9600  c537b420  c5c36360  REG   /var/log/news/errlog
      3  c74182c0  c6ede260  c6da3d40  PIPE
      4  c6df9720  c696c620  c69398c0  SOCK
      5  c6b9cc20  c68e7000  c6938d80  SOCK
      6  c6b9c920  c7cc45a0  c7c939e0  CHR   /dev/null
      7  c6b9c680  c58fa5c0  c58a1200  REG   /var/lib/news/history
      8  c6df9f00  c6ede760  c6da3200  PIPE
      9  c6b9c6e0  c58fa140  c5929560  REG   /var/lib/news/history.dir
     10  c7fa9320  c7fab160  c7fafd40  CHR   /dev/console
     11  c6b9c7a0  c58fa5c0  c58a1200  REG   /var/lib/news/history
     12  c377ec60  c58fa5c0  c58a1200  REG   /var/lib/news/history
     13  c4528aa0  c58fa6c0  c52fbb00  REG   /var/lib/news/history.pag
     14  c6df9420  c68e7700  c6938360  SOCK
     15  c6df9360  c68e7780  c6938120  SOCK
     16  c6b9c0e0  c68e7800  c6772000  SOCK
     17  c6b9c200  c6b5f9c0  c6b5cea0  REG   /var/lib/news/active
     21  c6b9c080  c6ede760  c6da3200  PIPE
 
  Display the files opened by the "crond" daemon, which is PID 462:

  crash> files 462
    PID: 462    TASK: f7220000  CPU: 2   COMMAND: "crond"
    ROOT: /    CWD: /var/spool
     FD    FILE     DENTRY    INODE    TYPE  PATH
      0  f7534ae0  f7538de0  f7518dc0  CHR   /dev/console
      1  f7368f80  f72c7a40  f72f27e0  FIFO  pipe:/[1456]
      2  f74f3c80  f72c79c0  f72f2600  FIFO  pipe:/[1457]
      3  f7368b60  f72a5be0  f74300c0  REG   /var/run/crond.pid
      4  f7534360  f73408c0  f72c2840  REG   /var/log/cron
      7  f7368ce0  f72c7940  f72f2420  FIFO  pipe:/[1458]
      8  f7295de0  f72c7940  f72f2420  FIFO  pipe:/[1458]
     21  f74f36e0  f747cdc0  f747e840  CHR   /dev/null
 
  The -R option is typically invoked from "foreach files".  This example
  shows all tasks that have "/dev/pts/4" open:

    crash> foreach files -R pts/4
    PID: 18633  TASK: c310a000  CPU: 0   COMMAND: "crash"
    ROOT: /    CWD: /home/CVS_pool/crash 
     FD    FILE     DENTRY    INODE    TYPE  PATH
      0  c1412850  c2cb96d0  c2cad430  CHR   /dev/pts/4
      1  c1412850  c2cb96d0  c2cad430  CHR   /dev/pts/4
      2  c1412850  c2cb96d0  c2cad430  CHR   /dev/pts/4
    
    PID: 18664  TASK: c2392000  CPU: 1   COMMAND: "less"
    ROOT: /    CWD: /home/CVS_pool/crash 
     FD    FILE     DENTRY    INODE    TYPE  PATH
      1  c1412850  c2cb96d0  c2cad430  CHR   /dev/pts/4
      2  c1412850  c2cb96d0  c2cad430  CHR   /dev/pts/4
    
    PID: 23162  TASK: c5088000  CPU: 1   COMMAND: "bash"
    ROOT: /    CWD: /home/CVS_pool/crash 
     FD    FILE     DENTRY    INODE    TYPE  PATH
      0  c1412850  c2cb96d0  c2cad430  CHR   /dev/pts/4
      1  c1412850  c2cb96d0  c2cad430  CHR   /dev/pts/4
      2  c1412850  c2cb96d0  c2cad430  CHR   /dev/pts/4
    255  c1412850  c2cb96d0  c2cad430  CHR   /dev/pts/4
    
    PID: 23159  TASK: c10fc000  CPU: 1   COMMAND: "xterm"
    ROOT: /    CWD: /homes/anderson/ 
     FD    FILE     DENTRY    INODE    TYPE  PATH
      5  c1560da0  c2cb96d0  c2cad430  CHR   /dev/pts/4
 
  Display information about the dentry at address f745fd60:

    crash> files -d f745fd60
     DENTRY    INODE    SUPERBLK  TYPE  PATH
     f745fd60  f7284640  f73a3e00  REG   /var/spool/lpd/lpd.lock
    """
    def __init__(self):
        parser = argparse.ArgumentParser(prog="files")

        parser.add_argument('-d', nargs=1)
        parser.add_argument('-R', nargs=1)
        parser.add_argument('args', nargs=argparse.REMAINDER)

        parser.format_usage = lambda : \
                    "files [-d dentry] | [-R reference] [pid | taskp] ...\n"

        CrashCommand.__init__(self, "files", parser)

    def execute(self, argv):
        vaddrfmt = "{1:^{0}}"
        files_header = " FD %s %s %s TYPE PATH" % (
                vaddrfmt.format(sz, "FILE"),
                vaddrfmt.format(sz, "DENTRY"),
                vaddrfmt.format(sz, "INODE"))

FilesCommand()
