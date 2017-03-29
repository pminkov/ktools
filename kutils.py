#!/usr/bin/python

import shlex
import subprocess
import sys

from kubernetes import client, config

config.load_kube_config()

commands = ['ssh', 'podmaps']

def print_commands():
  print 'kubeutils is a set of Kubernetes utility commands.'
  print
  print 'Commands:'
  print '  %-12s %s' % ('ssh', 'SSH to a pod')
  print '  %-12s %s' % ('podmaps', 'Print mapping from pod name to node name')

def ssh_to(pod_name):
  print 'SSH-ing to %s' % pod_name
  command = "kubectl exec -ti %s bash" % pod_name
  ret = subprocess.call(shlex.split(command))
  return ret

def command_ssh():
  v1 = client.CoreV1Api()
  ret = v1.list_pod_for_all_namespaces(watch=False)

  name = None
  if len(sys.argv) == 3:
    name = sys.argv[2]

  candidates = []
  for i in ret.items:
    if i.metadata.namespace != 'kube-system':
      if (not name) or (name in i.metadata.name):
        candidates.append(i.metadata.name)

  if len(candidates) == 0:
    print "No pods found with that name."
  elif len(candidates) == 1:
    ssh_to(candidates[0]);
  else:
    print "Multiple pods found:"
    for i in range(0, len(candidates)):
      print "%d) %s" % (i, candidates[i])
    choice = raw_input("Choice: ")
    index = int(choice)

    ssh_to(candidates[index]);

def command_podmaps():
  extra_params = ' '.join(sys.argv[2:])
  command = "kubectl get pods %s -o jsonpath='{range .items[*]}{.metadata.name} {.spec.nodeName}|{end}'" % extra_params
  output = subprocess.check_output(shlex.split(command))
  pods = output.split('|')[:-1]
  for pod in pods:
    (pod_name, node_name) = pod.split(' ')
    print '%-50s : %s' % (pod_name, node_name)


if __name__ == '__main__':
  name = None
  if len(sys.argv) == 1:
    print_commands()
  else:
    name = sys.argv[1]

    if not name in commands:
      print 'Invalid command'
      print 'Valid commands: ', commands.join(' | ')

    if name == 'ssh':
      command_ssh()
    elif name == 'podmaps':
      command_podmaps()
    

