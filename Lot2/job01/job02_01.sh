cp /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar .
./start-hadoop.sh
start-hbase.sh
hbase-daemon.sh start thrift
hdfs dfs -mkdir -p input
hdfs dfs -put data.csv input
hdfs dfs -rm -r outputjob02_01
hadoop jar hadoop-streaming-2.7.2.jar -file mapper1.py -mapper "python3 mapper1.py" -file reducer1.py -reducer "python3 reducer1.py" -input input/data.csv -output outputjob02_01
