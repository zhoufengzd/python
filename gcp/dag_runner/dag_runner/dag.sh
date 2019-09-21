#!/usr/bin/env bash
set -e
wk_dir=$(pwd)
script_dir="$(cd "$(dirname "$(readlink ${BASH_SOURCE[0]})")" && pwd)"
dag_runner_root="$(cd $script_dir/.. && pwd)"

action=$1
target=$2

function __help {
    script_name=$(basename "$0")
    echo "Usage: $script_name <action> <target=[config_file|dag_directory]>"
    echo "  action: support [build|run|deploy]"
    echo "  target: "
    echo "  -- config_file: dag config file."
    echo "  -- dag_directory: dag directory for google composer."
}

function __deploy {
    dag_dir=$1

    gcp_region=${GCP_REGION}
    gcp_project="${GCP_PROJECT:-${GOOGLE_CLOUD_PROJECT}}"
    gcp_composer=${gcp_project}-composer

    ## 2. upload to composer
    cmd="gcloud composer environments storage dags delete $dag_dir --quiet \
             --project $gcp_project --location $gcp_region --environment $gcp_composer"
    echo "" && echo $cmd && $cmd  > /dev/null

    cmd="gcloud composer environments storage dags import \
            --project $gcp_project --location $gcp_region --environment $gcp_composer \
            --source $dag_dir"
    echo "" && echo $cmd && $cmd
}

function main {
    if [ -z "$action" ] || [ -z "$target" ] || [[ $action == "-h" ]] || [[ $action == "--help" ]]; then
        __help && exit;
    fi

    ## env
    local pythonpath_old=$PYTHONPATH
    local wk_dir=$(pwd)
    local gcp_project="${GCP_PROJECT:-${GOOGLE_CLOUD_PROJECT}}"
    local gcp_region=${GCP_REGION}
    local gcp_composer=${gcp_project}-composer
    echo "-- @GCP_PROJECT=$gcp_project GCP_REGION=$gcp_region"

    start_time=$(date)
    if [[ $action == "deploy" ]]; then
        local dag_dir=$target
        if [ ! -e "$dag_dir" ]; then
            echo "Error! Directory \"$dag_dir\" does not exist!"
            exit
        fi

        local gcp_composer=${gcp_project}-composer
        cmd="gcloud composer environments storage dags delete $dag_dir --quiet \
                 --project $gcp_project --location $gcp_region --environment $gcp_composer"
        echo "" && echo $cmd #&& $cmd  > /dev/null
        cmd="gcloud composer environments storage dags import \
                --project $gcp_project --location $gcp_region --environment $gcp_composer \
                --source $dag_dir"
        echo "" && echo $cmd && $cmd
    else
        local config_file=$target
        if [ -e $dag_runner_root/venv/bin/activate ]; then source $dag_runner_root/venv/bin/activate && export PYTHONPATH=$dag_runner_root; fi
        cmd="python $dag_runner_root/dag_runner/job_executor.py $action $config_file"

        echo $cmd" ..." && $cmd
        if [ -e $dag_runner_root/venv/bin/activate ]; then deactivate && export PYTHONPATH="$pythonpath_old"; fi
    fi

    end_time=$(date)
    if [[ $action == "run" ]] || [[ $action == "deploy" ]]; then
        echo ""
        echo "--  started at $start_time"
        echo "--  stopped at $end_time"
    fi
}

main
