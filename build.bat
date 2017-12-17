:: batch
pushd `dirname $0` > /dev/null
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
popd > /dev/null
BUILDDIR="${SCRIPTPATH}/build"
GRFLEXLIBDIR="${SCRIPTPATH}/python/FlexlibMono"
FLEXLIBMONODIR="${SCRIPTPATH}/FlexlibMono"
FLEXLIBOUTPUTDIR="${FLEXLIBMONODIR}/tools"
FLEXLIBMONOBUILD="${FLEXLIBMONODIR}/buildtools.sh"

echo "Building FlexLibMono ${FLEXLIBMONOBUILD}"
/bin/bash "${FLEXLIBMONOBUILD}"

if [ ! -d "$GRFLEXLIBDIR" ]; then
    mkdir "$GRFLEXLIBDIR"
fi

echo "Copying FlexLibMono to gr-flex"
cp $FLEXLIBOUTPUTDIR/*.dll $GRFLEXLIBDIR

if [ ! -d "$BUILDDIR" ]; then
    mkdir "$BUILDDIR"
fi

cd "$BUILDDIR"

cmake ../
make
sudo make install
