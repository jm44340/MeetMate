UNAME=$(uname)
PYTHON=python

if [ "$UNAME" == "Linux" ] ; then
    PYTHON=python3
fi


pushd ./meetmate
pyreverse -A -o pdf -p meetmate \
  ./*.py \
  ./Widgets/* \
  ./AlgorithmsLogic/*
mv classes_meetmate.pdf ..
mv packages_meetmate.pdf ..
popd