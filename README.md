# Kubernetes Utils

#### ksh - ssh to a pod.

It's annoying to copy paste pod names when you want to ssh to a pod. Just use ksh.

```bash
$ python ./ksh.py jup
Multiple pods found:
0) jupyter-john-2
1) jupyter-petko-1
Choice: 0
SSH-ing to jupyter-john-2
root@jupyter-ivan-2:/# uname -r
4.4.21+
```
