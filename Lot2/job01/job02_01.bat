docker cp mapper1.py hadoop-master:/root/
docker cp reducer1.py hadoop-master:/root/
docker cp data.csv hadoop-master:/root/
docker cp job02_01.sh hadoop-master:/root/
docker exec hadoop-slave1 /bin/bash -c './service_slv.sh'
docker exec hadoop-slave2 /bin/bash -c './service_slv.sh'
docker exec hadoop-master /bin/bash -c './job02_01.sh'