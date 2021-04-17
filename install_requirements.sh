UNAME=$(uname)
PYTHON=python

if [ "$UNAME" == "Linux" ] ; then
    PYTHON=python3
fi

$PYTHON -m pip install --upgrade pip
$PYTHON -m pip install -r requirements.txt