import subprocess
import sys
import setup_util
import os

def start(args):
  setup_util.replace_text("snap/bench/cfg/db.cfg", "host=\".*\"", "host=\"" + args.database_host + "\"")
  subprocess.check_call("cabal install HDBC HDBC-mysql MonadCatchIO-transformers configurator json snap-core snap-server resource-pool", shell=True)  
  subprocess.check_call("cabal configure", shell=True, cwd="snap/bench")
  subprocess.check_call("cabal install", shell=True, cwd="snap/bench")

  subprocess.Popen("dist/build/snap-bench/snap-bench +RTS -N" + str(args.max_threads) + " > /dev/null", shell=True, cwd="snap/bench")
  return 0

def stop():
  p = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
  out, err = p.communicate()
  for line in out.splitlines():
    if 'snap-bench' in line:
      try:
        pid = int(line.split(None, 2)[1])
        os.kill(pid, 9)
      except OSError:
        pass

  return 0
