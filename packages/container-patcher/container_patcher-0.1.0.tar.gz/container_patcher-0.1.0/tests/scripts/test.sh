#! /bin/bash

if ! [ -d ./binnacle-icse2020 ]; then
    git clone https://github.com/jjhenkel/binnacle-icse2020.git
fi

if ! [ -d ./sources-gold ]; then
    tar -xvf binnacle-icse2020/datasets/0a-original-dockerfile-sources/gold.tar.xz
fi

for ((i=0; i < 1; i++)); do
    file_name=`ls sources-gold | sed -n $(($RANDOM % 433))P`
    rand_num=`echo ${file_name} | tr '.' '\n' | sed -n 1P`

    if [ -d ./test_${rand_num} ]; then
        break
    fi
    mkdir test_${rand_num}
    mv ./sources-gold/${file_name} ./test_${rand_num}
    mv ./test_${rand_num}/${file_name} ./test_${rand_num}/Dockerfile
    docker build -t "${rand_num}-testimage" ./test_${rand_num}
    docker run -itd --name "${rand_num}-testcontainer" "${rand_num}-testimage"
    dist_name=`docker exec ${rand_num}-testcontainer cat /etc/issue | tr ' ' '\n' | sed -n 1P`
    if [ $dist_name = "Debian" ]; then
        if ! [ -d ./logfiles ]; then
            mkdir ./logfiles
         fi;
        trivy ${rand_num}-testimage
    fi
done
