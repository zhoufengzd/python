wk_dir=$(pwd)
cd ../_data/generated

for dt in $(ls *.csv); do
    echo ${dt}
    cmd="bq.sh i people.experience_data_bytes=${dt}"
    echo $cmd && $cmd
done

cd ${wk_dir}
