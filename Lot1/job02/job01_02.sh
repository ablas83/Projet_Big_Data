cp /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar .
./start-hadoop.sh
start-hbase.sh
hbase-daemon.sh start thrift
hdfs dfs -mkdir -p input
hdfs dfs -rm input/data.csv
hdfs dfs -put data.csv input
hdfs dfs -rm -r outputjob01_02
hadoop jar hadoop-streaming-2.7.2.jar -file mapper2.py -mapper "python3 mapper2.py" -file reducer2.py -reducer "python3 reducer2.py" -input input/data.csv -output outputjob01_02
