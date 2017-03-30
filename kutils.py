#!/usr/bin/python

import os
import shlex
import subprocess
import sys

from kubernetes import client, config

config.load_kube_config()

commands = ['ssh', 'podmaps', 'instance-group']

global argv

class ArgvConsumer:
  def __init__(self):
    self.position = 1

  def done(self):
    return self.position >= len(sys.argv)

  def get_value(self, value_name):
    if self.done():
      print 'Missing argument: %s.' % value_name
      sys.exit(0)

    ret = sys.argv[self.position]
    self.position += 1
    return ret

def print_commands(with_intro=True):
  if with_intro:
    print 'kubeutils is a set of Kubernetes utility commands.'
    print
  print 'Commands:'
  print '  %-16s %s' % ('ssh', 'SSH to a pod')
  print '  %-16s %s' % ('podmaps', 'Print mapping from pod name to node name')
  print
  print 'Kubernetes on Google Container Engine (GKE) commands:'
  # print '  %-16s %s' % ('resize-wait', 'Resizes a cluster and waits until resize is done')
  print '  %-16s %s' % ('instance-group', 'Get instance group name for a cluster')
  print

def ssh_to(pod_name):
  print 'SSH-ing to %s' % pod_name
  command = "kubectl exec -ti %s bash" % pod_name
  ret = subprocess.call(shlex.split(command))
  return ret

def command_ssh():
  v1 = client.CoreV1Api()
  ret = v1.list_pod_for_all_namespaces(watch=False)

  name = None
  if not argv.done():
    name = argv.get_value('name')

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


def command_instance_group():
  dir_path = os.path.dirname(os.path.realpath(__file__))
  script_path = os.path.join(dir_path, "scripts/instance-group.sh")

  cluster = argv.get_value("cluster")

  ret = subprocess.check_output(shlex.split(script_path + " " + sys.argv[2]))
  print ret


if __name__ == '__main__':
  name = None
  argv = ArgvConsumer()

  if argv.done():
    print_commands()
  else:
    name = argv.get_value("command")

    if not name in commands:
      print 'Invalid command: %s.' % name
      print
      print_commands(with_intro=False)

    if name == 'ssh':
      command_ssh()
    elif name == 'podmaps':
      command_podmaps()
    elif name == 'instance-group':
      command_instance_group()
    

