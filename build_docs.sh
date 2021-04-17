UNAME=$(uname)
PYTHON=python

if [ "$UNAME" == "Linux" ] ; then
    PYTHON=python3
fi

rm -rv ./docs/*
pushd ./meetmate
$PYTHON -m pdoc --output-dir ../docs --html . 
popd
mv -v ./docs/meetmate/* ./docs
rmdir ./docs/meetmate