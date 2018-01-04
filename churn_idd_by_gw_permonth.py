#! /usr/bin/python
# -*- coding: utf-8 -*-
# Author fouad@genunsys.com 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


"""
 output file is 'churn_users.txt'. It holds all idd.
 the database is queried by months
 the output of each query is stored in a common set of idd. The values in a set are all unique.
  finally we write the contents of the set to the output file
"""

import MySQLdb
import sys
import yaml
from datetime import datetime

# read configuration values for mysql_server.conf
# the config is assumed to be in yaml format
# for ini like config file, use ConfigParser

config = yaml.load(open('mysql_setting.conf'))
remote = config.get('remote', {})
remote_server = remote.get('server', '')
remote_user = remote.get('user', '')
remote_password = remote.get('password', '')
remote_db = remote.get('database', '')

output_file = 'churn_users.csv'

try:
    # create a connection to remote database using config values
    # the commands are executed and using the cursor object
    conn = MySQLdb.connect(host=remote_server, user=remote_user, passwd=remote_password, db=remote_db)
    cursor = conn.cursor()
    output = dict()
    outputfile = open(output_file, 'w')
    

    year = '2017' #Try to get the list of Idd with GW that used our service from june to Aug 
    for month in range(6,9):
        print month                 
            
      
        cursor.execute("""
select
        idd,
        Gw,
        count(*),
        sum(seconds) as secs
from `db`.`table1`
where month(date_start) = %s 
        and year(date_start) = %s
group by idd, Gw
having count(*) > 2 and secs > 179 
        """ % (str(month), str(year)))
        print 'endquery!!!!'
        idd_list = []
        idd_list =  cursor.fetchall()
        for idd in idd_list:
            # idd -> (idd, Gw, count, secs)
            # if the (idd, Gw) pair exists, then add the secs and the count
            count_secs = output.get((idd[0], idd[1]), None)
            if count_secs:
                output[(idd[0], idd[1])][0] += idd[2]
                output[(idd[0], idd[1])][1] += idd[3]
            else:
                output[(idd[0], idd[1])] = [idd[2], idd[3]]

    outputfile.write(','.join(['idd', 'Gw', 'count', 'secs']) + '\n')
    for j in output.keys():
        idd, gw = j
        count,secs = output[j]
        outputfile.write(','.join([str(idd), str(Gw)]) + '\n')
        outputfile.flush()
    outputfile.close()
        
except Exception as e:
    print e
    print 'Something went wrong.\n Check the commands'
