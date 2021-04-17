UNAME=$(uname)
PYTHON=python

if [ "$UNAME" == "Linux" ] ; then
    PYTHON=python3
fi

pushd meetmate
FLASK_APP=meetmate.py FLASK_ENV=development FLASK_DEBUG=1 $PYTHON -m flask run
popd