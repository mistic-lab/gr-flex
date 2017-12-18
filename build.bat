:: batch
:: Do we need this if we tell them what folder to execute the script from?
pushd %~dp0 1> NUL
set SCRIPTPATH=%CD%
popd 1> NUL

set BUILDDIR=%SCRIPTPATH%\build
set GRFLEXLIBDIR=%SCRIPTPATH%\python\FlexlibMono
set FLEXLIBMONODIR=%SCRIPTPATH%\FlexlibMono
set FLEXLIBOUTPUTDIR=%FLEXLIBMONODIR%\tools
set FLEXLIBMONOBUILD=%FLEXLIBMONODIR%\buildtools.bat

echo "Building FlexLibMono %FLEXLIBMONOBUILD%"
call %FLEXLIBMONOBUILD%

if not exist %GRFLEXLIBDIR% mkdir %GRFLEXLIBDIR%

echo "Copying FlexLibMono to gr-flex"
copy %FLEXLIBOUTPUTDIR%/*.dll %GRFLEXLIBDIR%

if not exist %BUILDDIR%  mkdir %BUILDDIR%

cd %BUILDDIR%

cmake ../
make
sudo make install
