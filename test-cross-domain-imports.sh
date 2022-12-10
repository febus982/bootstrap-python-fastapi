#!/usr/bin/env bash
shopt -s extglob

export CROSSIMPORTFOUND=0

cd app/domains


for dir in $(ls -d !(__pycache__)/ )
do
  echo "DIR=$dir"
  regex="app\.domains(?!\.${dir::-1}\.)"
  echo "$regex"
  for file in $(find ${dir} -type f -name '*.py')
  do
    grep -nH -P "${regex}" $file
    if [ $? -eq 0 ]
    then
      CROSSIMPORTFOUND=1
    fi
  done
done

if [ $CROSSIMPORTFOUND -eq 1 ]
then
  echo "Nested domain module or wider 'app.domains' import detected."
fi

exit $CROSSIMPORTFOUND
