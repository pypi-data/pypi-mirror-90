#!/bin/bash

# the `pipefail` below is the only reason why we use `bash` instead of
# `/bin/sh`, otherwise the script is POSIX compliant.  We need `pipefail`
# because of the frquent use of piping to `progress`.
set -o pipefail


# TODO:
#  - on first of each months, remove all environments which are not used for
#    longer than 30 days.  To support that, each use should update a timestamp.
#  - use a lockfile to ensure only one bootstrapper is active at any time in
#    a specific environment dir.

# ------------------------------------------------------------------------------
#
# Create a conda env under $RC_BASE/bootstrap/envs/, and install `rc.bootstrap`
# and `rc.utils` in it.
#
# This script takes the following arguments (shown are default settings):
#
#    -b: home of RC environments
#        $HOME/.rc/bootstrap/envs/
#    -c: URL to fetch miniconda from
#        https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
#    -i: packages to install
#        ''
#    -r: command to run after completion
#        ''
#    -n: name of environment to bootstrap
#        rc.$RC_BOOTSTRAP_VERSION
#    -p: pre-exec commands to run before environment setup
#        ''
#
# Note that the conda url should point to a suitable architecture, matching the
# resource the bootstrapper is running on. `-p` and `-i` can be specified
# multiple times.
#
# All arguments are expanded with the environment of the shell running this
# script (usually the login shell).  The variable `RC_BOOTSTRAP_VERSION` will be
# automatically set to the version of the `rc.bootstrap` module and cannot be
# overwritten.
#
# Arguments passed to `-i` can have different formats (distingushed by URL
# schemas), and will be installed in different ways:
#
#   - conda:<name>
#     conda wheel name
#     install: conda install -y <name>
#     example: conda:pandas
#
#   - pypi:<module_name>
#     pypi module name
#     install: `pip install <module_name>
#     example: numpy
#
#   - tar:<file_name>
#     tarball in the current working directory
#     install: tar xf <file_name>
#              pip install <file_base>
#     where <file_base> is <file_name> without extensions like `tgz`, `tar`,
#     `tar.gz` etc.
#     example: numpy.tar.gz
#              numpy-1.2.3.tgz
#
#   - pip:<url>
#     source location
#     install: pip install <url>
#     example: git+https://github.com/project/repo/branch/devel
#
# The argument passed to `-r` is `exec`ed after bootstrapping completed
# successfully.  That command will inherit pid and stdio handles from the
# bootstrapper process.
#
LOG=$(mktemp)

# ------------------------------------------------------------------------------
#
out(){
    printf "$*" >> $LOG
    printf "$*"
}

err(){
    out "# \n"
    printf "ERROR: $*\n$LOG\n" >> $LOG
    printf "ERROR: $*\n$LOG\n" 1>&2
    out "# \n"
    out "# ---------------------------------------------------------------\n"
    exit 1
}

check() {
    ret="$1"; shift
    log="$*"
    if test "$ret" = "0"
    then
        out "#\n# OK\n"
    else
        err "$log failed"
    fi
}


# ------------------------------------------------------------------------------
#
progress(){

    printf "# ["
    while read X
    do
        echo "$X" >> $LOG
        echo -n "."
    done
    printf "]\n"
}


# ------------------------------------------------------------------------------
#
pre_exec() {
    cmd="$*"
    out "#\n"
    out "# ---------------------------------------------------------------\n"
    out "#\n# run pre_exec: $cmd\n#\n"
    eval "$cmd" 2>&1 | progress
    check "$?" "pre_exec $cmd"
}


# ------------------------------------------------------------------------------
#
post_install() {
    spec="$1"

    out "# \n"
    out "# -------------------------------------------------------------------\n"
    out "#\n# post-install $spec\n#\n"
    schema=$(echo "$spec" | cut -f 1  -d ':')
    name=$(  echo "$spec" | cut -f 2- -d ':')

    if test "$schema" = "conda"
    then
        conda install -y "$name" 2>&1 | progress
        res=$?
    elif test "$schema" = "pypi"
    then
        pip install "$name" 2>&1 | progress
        res=$?
    elif test "$schema" = "tar"
    then
        dname="$name"
        dname=$(basename "$dname" .tgz)
        dname=$(basename "$dname" .tbz)
        dname=$(basename "$dname" .gz)
        dname=$(basename "$dname" .bz)
        dname=$(basename "$dname" .bz2)
        dname=$(basename "$dname" .tar)
           tar xf "$name"       2>&1 | progress \
        && pip install "$dname" 2>&1 | progress
        res=$?
    elif test "$schema" = "pip"
    then
        set -x
        pip install "$name" 2>&1 | progress
        set +x
        res=$?
    else
        err "invalid post-install schema in '$spec'"
    fi

    check "$res" "post_install $spec"
}


# ------------------------------------------------------------------------------
# set defaults
RC_VERSION='0.1.0'
RC_VERSION='0.0.0'
RC_BASE="$HOME/.rc"
RC_NAME="rc.$RC_VERSION"
RC_EXEC=""
CONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
PRE_EXEC=''

# get paratemeter settings
while getopts "b:c:i:n:p:r:" OPTION; do
    case $OPTION in
        b)  RC_HOME="$OPTARG"          ;;
        c)  CONDA_URL="$OPTARG"        ;;
        i)  INSTALL="$INSTALL $OPTARG" ;;
        n)  RC_NAME="$OPTARG"          ;;
        p)  pre_exec "$OPTARG"         ;;
        r)  RC_EXEC="$OPTARG"          ;;
        *)  err "Unknown option: '$OPTION'='$OPTARG'" 2>&1
    esac
done

# expand env variables.
RC_BASE=$(eval echo "$RC_BASE")
RC_NAME=$(eval echo "$RC_NAME")
CURL_URL=$(eval echo "$CURL_URL")

# get conda script name
CONDA_SCRIPT=$(echo "$CONDA_URL" | sed -e 's|^.*/||g')

# ensure we have what we need
test -z "$CONDA_URL" && err 'missing conda url'

# ensure we have a conda fetcher
CURL=$(which curl)
WGET=$(which wget)

# create a envs/' dir under $RC_BASE
ENV_LOC="$RC_BASE/bootstrap/envs/$RC_NAME"

out "# -------------------------------------------------------------------\n"
out "#\n# check setup\n#\n"
out "RC_VERSION   : $RC_VERSION  \n"
out "RC_BASE      : $RC_BASE     \n"
out "RC_NAME      : $RC_NAME     \n"
out "CONDA_URL    : $CONDA_URL   \n"
out "CONDA_SCRIPT : $CONDA_SCRIPT\n"
out "CURL         : $CURL        \n"
out "WGET         : $WGET        \n"
out "ENV_LOC      : $ENV_LOC     \n"

mkdir -p   "$RC_BASE/bootstrap"
cd         "$RC_BASE/bootstrap"

out "# -------------------------------------------------------------------\n"
out "#\n# fetch miniconda\n"
if test -f "$CONDA_SCRIPT"
then
    out "# using cached script\n#\n"
else
    if ! test -z "$WGET"
    then
        out "# using $WGET $CONDA_URL\n#\n"
        "$WGET" -nv -O "$CONDA_SCRIPT" "$CONDA_URL" 2>&1 | progress
        check "$?" "wget"
    elif ! test -z "$CURL"
    then
        out "# using $CURL $CONDA_URL\n#\n"
        "$CURL" -s -o "$CONDA_SCRIPT" "$CONDA_URL" 2>&1 | progress
        check "$?" "curl"
    else
        err 'missing curl / wget'
    fi
fi


out "# -------------------------------------------------------------------\n"
out "#\n# install miniconda\n"
if test -x "$ENV_LOC/miniconda/bin/python3.8"
then
    out "# skipped - install exists\n"
else
    /bin/sh "$CONDA_SCRIPT" -b -f -p $(pwd)/miniconda -s -u 2>&1 | progress
    check "$?" "minicondafailed"
fi

out "# \n"
out "# -------------------------------------------------------------------\n"
out "#\n# activate miniconda\n#\n"
. miniconda/etc/profile.d/conda.sh

out "# \n"
out "# -------------------------------------------------------------------\n"
out "#\n# create env $RC_NAME\n#\n"
conda create -y -p "$ENV_LOC" 2>&1 | progress
check "$?" "miniconda failed"

out "# \n"
out "# -------------------------------------------------------------------\n"
out "#\n# activate env $RC_NAME\n#\n"
eval "$(conda shell.bash hook)"
check "$?" "activate hook failed"
conda activate "$ENV_LOC" 2>&1 | progress
check "$?" "activate failed"

out "# -------------------------------------------------------------------\n"
out "#\n# install rc.bootstrap\n#\n"
pip install rc.bootstrap 2>&1 | progress
check "$?" "pip install 'rc.bootstrap'"

out "# \n"
out "# -------------------------------------------------------------------\n"
out "#\n# install rc.utils\n#\n"
pip install rc.utils 2>&1 | progress
check "$?" "pip install 'rc.utils'"

out "# \n"
out "# -------------------------------------------------------------------\n"
out "#\n# summary\n#\n"
conda info
rc.stack
check "$?" "environment check"

# basic bootstrapping is done, the environment is valid. Install additional
# modules
for spec in $INSTALL
do
    post_install "$spec"
done

# Finally, capture that envirnment (including the `pre_exec` commands executed
# earlier).  We use the `radical.utils` env isolation facilities for that, which
# we know we installed as dependency of `rc.utils`.
out "# \n"
out "# -------------------------------------------------------------------\n"
out "#\n# capture environment\n#\n"
# TODO
check "$?" "capture environment"
out "# \n"
out "# -------------------------------------------------------------------\n"

mv -i "$ENV_LOC/log" "$ENV_LOC/log.1" 2>/dev/null || true
mv -i $LOG           "$ENV_LOC/log"

out "# \n"
out "# -------------------------------------------------------------------\n"
out "#\n# execute command\n#\n"
if test -z "$RC_EXEC"
then
    out "no command specified\n"
else
    exec $RC_EXEC
    # we should never get here...
    check "1" "execute command"
fi
out "# \n"
out "# -------------------------------------------------------------------\n"

# ------------------------------------------------------------------------------

