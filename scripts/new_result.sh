#!/bin/bash
# run this script after a new experiment to archive logs and run analyses

# OPTIONS
rootdir="/root/pirel-code"
logsdir="/root/pirel-shared-volume/logs-archive"
expid="debug-49"
subject_names_fpath="${rootdir}/experiments/subjects-names.txt"

# PREPARATIONS
mapfile -t subject_names < "$subject_names_fpath"
dhdir="${logsdir}/${expid}"
mkdir -p $dhdir

# MOVING LOGS
cd $rootdir
mv logs $dhdir
git checkout logs

# REPLACING PATHS
cd $dhdir/logs
cp pirel.log orig.pirel.log  # backup
sed -i 's|'"$rootdir"'|'"$dhdir"'|g' pirel.log

# SPLITTING LOGS
for subject_name in "${subject_names[@]}";
do
    echo "(grep) Processing $subject_name"
    grep $subject_name pirel.log > "${subject_name}.log"
    mv "${subject_name}.log" learn-rules/
done

# RUNNING ANALYSES
cd $rootdir/src
python e_logs_analyze.py \
-a 1 \
-s "${subject_names_fpath}" \
-l "${dhdir}/logs/learn-rules" \
-t debug-49-learn-apply-error

python e_logs_analyze.py \
-a 2 \
-s "${subject_names_fpath}" \
-l "${dhdir}/logs/learn-rules" \
-t debug-49-input-output-tokens
