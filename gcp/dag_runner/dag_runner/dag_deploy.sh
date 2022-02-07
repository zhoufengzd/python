#!/bin/bash
set -e

wk_dir=$(pwd)

## 1. set environment
dag_source_dir=$1
gcp_project=${GCP_PROJECT:-${GOOGLE_CLOUD_PROJECT:-${PROJECT}}}

default_ifs="$IFS"
IFS="| " composer_config=($(gcloud composer environments list --locations=us-west1,us-west2,us-east1 | grep RUNNING))
IFS=$default_ifs
gcp_composer=${composer_config[1]}
gcp_region=${composer_config[3]}

## 2. upload to composer
function __deploy {
    local dag_dir="$1"
    echo dag_dir=$dag_dir
    cmd="gcloud composer environments storage dags delete $dag_dir --quiet \
             --project $gcp_project --location $gcp_region --environment $gcp_composer"
    echo "" && echo $cmd && $cmd  > /dev/null

    cmd="gcloud composer environments storage dags import \
            --project $gcp_project --location $gcp_region --environment $gcp_composer \
            --source $dag_dir"
    echo "" && echo $cmd && $cmd
}

if [ ! -z $dag_source_dir ]; then
    if [ ! -d $dag_source_dir ]; then
        dag_source_dir="_generated/airflow/"${dag_source_dir//".yaml"/}
    fi
fi

if [ -z $dag_source_dir ] || [ ! -d $dag_source_dir ]; then
    echo "Usage: dag_deploy.sh <dag source directory>"
else
    cd $dag_source_dir && dag_dir=${PWD##*/} && cd .. && echo "" && echo "-- @$(pwd)"
    __deploy $dag_dir
    cd $wk_dir
fi
