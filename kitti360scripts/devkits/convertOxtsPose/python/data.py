import os
import numpy as np

def loadOxtsData(oxts_dir, frames=None):
  ''' reads GPS/IMU data from files to memory. requires base directory
  (=sequence directory as parameter). if frames is not specified, loads all frames. '''

  ts = []

  if frames is None:

    ts = loadTimestamps(oxts_dir)
    oxts  = []
    for i in range(len(ts)):
      if len(ts[i]):
        try:
          oxts.append(np.loadtxt(os.path.join(oxts_dir, 'data', '%010d.txt'%i)))
        except:
          oxts.append([])
      else:
        oxts.append([])

  elif len(frames)>1:
    k = 1
    oxts = []
    for _ in range(len(frames)):
      try:
        oxts.append(np.loadtxt(os.path.join(oxts_dir, 'data', '%010d.txt'%k)))
      except:
        oxts.append([])
      k=k+1

  else:
    file_name = os.path.join(oxts_dir, 'data', '%010d.txt'%k)
    try:
      oxts = np.loadtxt(file_name)
    except:
      oxts = []

  return oxts,ts

def loadTimestamps(ts_dir):
  ''' load timestamps '''

  with open(os.path.join(ts_dir, 'timestamps.txt')) as f:
      data=f.read().splitlines()
  return [l.split(' ')[0] for l in data]

def loadPoses (pos_file):
  ''' load system poses '''

  data = np.loadtxt(pos_file)
  ts = data[:, 0].astype(np.int)
  poses = np.reshape(data[:, 1:], (-1, 3, 4))
  poses = np.concatenate((poses, np.tile(np.array([0, 0, 0, 1]).reshape(1,1,4),(poses.shape[0],1,1))), 1)
  return ts, poses

