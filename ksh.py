import shlex
import subprocess
import sys

from kubernetes import client, config

config.load_kube_config()

def ssh_to(pod_name):
  print 'SSH-ing to %s' % pod_name
  command = "kubectl exec -ti %s bash" % pod_name
  ret = subprocess.call(shlex.split(command))
  return ret
  

if __name__ == '__main__':
  name = None
  if len(sys.argv) == 2:
    name = sys.argv[1]
    
  v1 = client.CoreV1Api()
  ret = v1.list_pod_for_all_namespaces(watch=False)

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


