pushd `dirname $0` > /dev/null
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
popd > /dev/null
BUILDDIR="${SCRIPTPATH}/build"

if [ ! -d "$BUILDDIR" ]; then
    mkdir "$BUILDDIR"
fi

cd "$BUILDDIR"

cmake ../
make
sudo make install

