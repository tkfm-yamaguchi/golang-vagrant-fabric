from fabric.api import run, cd
from fabric.contrib.files import append, exists
from fabric.context_managers import shell_env


# install_golang:
#   Compile and install Go 1.5 with bootstrappnig by Go 1.4.
#
#   This function creates the directories below:
#
#       ~/local/        : directory for GOPATH
#           pkg/golang/ : directory to place Go sources
#               go1.4/  : Go 1.4 binaries with sources which downloaded
#               repo/   : Go source repository to compile/install


def setup():
    install_golang()


def install_golang():
    with cd('~'):
        if not exists('local/pkg/golang'):
            run('mkdir -p local/pkg/golang')


    with cd('~/local/pkg/golang'):
        if exists('go1.4'): run('rm -rf go1.4')

        run('mkdir go1.4')
        run('wget https://storage.googleapis.com/golang/go1.4.2.linux-amd64.tar.gz')
        run('tar zxf go1.4.2.linux-amd64.tar.gz -C go1.4 --strip-components 1')
        run('mv go1.4.2.linux-amd64.tar.gz go1.4')


    with cd('~/local/pkg/golang'):
        if exists('repo'): run('rm -rf repo')

        run('git clone https://go.googlesource.com/go repo')


    with cd('~/local/pkg/golang/repo/src'):
        run('GOROOT_BOOTSTRAP="$HOME/local/pkg/golang/go1.4" ./all.bash')


    with cd('~'):
        for rcfile in ['.bashrc', '.bashrc.local']:
            if not exists(rcfile): run('touch %s' % rcfile)

        append('~/.bashrc', 'source .bashrc.local')
        append('~/.bashrc.local', '''
# Settings for Go
export GOPATH="$HOME/local"
export PATH="$HOME/local/pkg/golang/repo/bin:$PATH"''')
