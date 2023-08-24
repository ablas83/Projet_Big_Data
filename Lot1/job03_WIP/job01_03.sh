cp /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar .
./start-hadoop.sh
start-hbase.sh
hbase-daemon.sh start thrift
hdfs dfs -mkdir -p input
hdfs dfs -put data.csv input
hdfs dfs -rm -r outputjob01_03
hadoop jar hadoop-streaming-2.7.2.jar -file mapper3.py -mapper "python3 mapper3.py" -file reducer3.py -reducer "python3 reducer3.py" -input input/data.csv -output outputjob01_03
