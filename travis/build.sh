#!/bin/bash
echo '######################################'
echo '#                Build               #'
echo '#              - START -             #'
echo '######################################'

echo "Creating pdf output ..."
pwd
cd ./tuto
pwd
pandoc --from=markdown+yaml_metadata_block -t html5 --template=../pandoc/pandoc_tpl.html -s tuto.md -o ${TRAVIS_BUILD_DIR}/tuto.pdf

echo '######################################'
echo '#                Build               #'
echo '#            - FINISHED -            #'
echo '######################################'
