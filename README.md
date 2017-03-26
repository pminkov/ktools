# Kubernetes Utils

#### ksh - ssh to a pod.

It's annoying to copy and paste pod names when you want to ssh to a pod. You can use ksh instead.

```bash
$ ./ksh jup
Multiple pods found:
0) jupyter-john-2
1) jupyter-petko-1
Choice: 0
SSH-ing to jupyter-john-2
root@jupyter-john-2:/# uname -r
4.4.21+
```
