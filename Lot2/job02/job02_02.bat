docker cp mapper2.py hadoop-master:/root/
docker cp reducer2.py hadoop-master:/root/
docker cp data.csv hadoop-master:/root/
docker cp job02_02.sh hadoop-master:/root/
docker exec hadoop-slave1 /bin/bash -c './service_slv.sh'
docker exec hadoop-slave2 /bin/bash -c './service_slv.sh'
docker exec hadoop-master /bin/bash -c './job02_02.sh'