#!/usr/bin/python3

import csv
import os
import sys

msg = """
[-------------------------------------]
|    WAZUH Agent Removal Script       |
[-------------------------------------]
"""

print(msg)

if len(sys.argv) < 2:
  print("usage: python " +sys.argv[0]+ " [csv_file_name]\n")
  sys.exit(1)

agent_list = []

try:
  csvFile = csv.reader(open(sys.argv[1], "rt"))
except IOError:
    print('csv file not found\n')
    sys.exit(1)    

for row in csvFile:
  agent_list.append(row[1])

final_agent_id = agent_list[1::]

print(final_agent_id)

usrip = input(f"\n {len(final_agent_id)} Agents will be Deleted want to continue (y/n) : ")

if (usrip == 'yes' or usrip == 'Y' or usrip == 'y'):

  for id in final_agent_id:
    try:
        os.system(f'/var/ossec/bin/manage_agents -r {id}')
        print(f'Agent : {id} Successfully Kick out !')

    except Exception as e:
      sys.exit(1)

  print(f'\nscript executed successfully')

else:
  print(f'\nOperation Aborted !!')
  sys.exit(1)    

