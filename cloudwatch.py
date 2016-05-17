import boto3
import boto.ec2.cloudwatch
import boto.ec2
import sys
import argparse
import datetime
import sqlite3
from pprint import pprint

# Connect to boto.ec2.connection
connEc2 = boto.ec2.connection.EC2Connection()
# Connect to cloudwatch endpoint
conn = boto.ec2.cloudwatch.connect_to_region('us-east-1')
if conn == None:
		exit_with_error('Unable to connect to AWS endpoint for region %s' % region_name)

	# Retrieve the relevant metrics	
billing_metrics = conn.list_metrics(metric_name=u'EstimatedCharges', namespace=u'AWS/Billing')
	# Retrieve the relevant metrics, ec2 instances get_all_instance_status
ec2_metrics = connEc2.get_all_instance_status(include_all_instances=True)

print ec2_metrics


now = datetime.datetime.now()
today = datetime.datetime(now.year, now.month, now.day)
#ttt = datetime.datetime.now() - datetime.timedelta(hours=1)
for metric in billing_metrics:
	if u'ServiceName' in metric.dimensions:
		if metric.dimensions['ServiceName'] == [u'AmazonEC2']:
			datapoints = metric.query(today, now, ['Maximum', 'Sum'])
			datapoints = sorted(datapoints, key=lambda datapoint: datapoint[u'Timestamp'], reverse=True)
			print("%s:" % metric.dimensions['ServiceName'][0])
			if len(datapoints) != 0:
			    print (datapoints[0])[u'Maximum']
			    print
