#! /bin/bash

ROOT_DIR=$(pwd)
SRC_DIR=${ROOT_DIR}/src
LOGS_DIR=${ROOT_DIR}/logs
cd ${ROOT_DIR}

# should be run from `pyjs` branch
git checkout pyjs

# reset logs directory
cd ${LOGS_DIR}
mv learn-rules/.gitignore /tmp/.gitignore.learn-rules
rm -rf learn-rules/*
mv /tmp/.gitignore.learn-rules learn-rules/.gitignore
mv pirel/.gitignore /tmp/.gitignore.pirel
rm -rf pirel/*
mv /tmp/.gitignore.pirel pirel/.gitignore
rm -f *.log

# run PiREL for Python-JavaScript
echo "Running PiREL for Python-JavaScript..."
cd ${SRC_DIR}
python p_learn_apply_rules.py \
--benchmark-name gfg \
--src-lang py \
--tar-lang js \
--is-three-split \
--sample-size 50 \
2> /dev/null

# copy logs to a separate folder
cd ${ROOT_DIR}
cp -r logs logs-pyjs
cd ${LOGS_DIR}
mv learn-rules/.gitignore /tmp/.gitignore.learn-rules
rm -rf learn-rules/*
mv /tmp/.gitignore.learn-rules learn-rules/.gitignore
mv pirel/.gitignore /tmp/.gitignore.pirel
rm -rf pirel/*
mv /tmp/.gitignore.pirel pirel/.gitignore
rm -f *.log
cd ${ROOT_DIR}

# count progress
cd logs-pyjs/learn-rules
echo "Success rate is $(ls -1 | grep apply_phase_success | wc -l)/50"
cd ${ROOT_DIR}

echo "Done running PiREL for Python-JavaScript."
