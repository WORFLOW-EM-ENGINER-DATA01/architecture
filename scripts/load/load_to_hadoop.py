from scripts.load.storm_events import load_storm_events_to_hadoop
from scripts.load.gsod import load_gsod_to_hadoop
from hdfs import InsecureClient

hdfs_client = InsecureClient('http://localhost:9870', user='root')

load_storm_events_to_hadoop(hdfs_client)
load_gsod_to_hadoop(hdfs_client)