docker cp mapper3.py hadoop-master:/root/
docker cp reducer3.py hadoop-master:/root/
docker cp data.csv hadoop-master:/root/
docker cp job01_03.sh hadoop-master:/root/
docker exec hadoop-slave1 /bin/bash -c './service_slv.sh'
docker exec hadoop-slave2 /bin/bash -c './service_slv.sh'
docker exec hadoop-master /bin/bash -c './job01_03.sh'