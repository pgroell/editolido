#!/bin/bash
echo '######################################'
echo '#                Build               #'
echo '#              - START -             #'
echo '######################################'

echo "Creating pdf output ..."
pwd
ls -al ${PWD}/wkhtmltopdf/wkhtmltox/bin/
cd ./tuto
echo $PATH
pandoc --from=markdown+yaml_metadata_block -t html5 --template=../pandoc/pandoc_tpl.html -s tuto.md -o ${TRAVIS_BUILD_DIR}/tuto.html
wkhtmltopdf tuto.html tuto.pdf

echo '######################################'
echo '#                Build               #'
echo '#            - FINISHED -            #'
echo '######################################'
