
def unique(a):
  '''
  return the list with duplicate elements removed
  '''
  return list(set(a))

def intersect(a, b):
  '''
  return the intersection of two lists
  '''
  return list(set(a) & set(b))

def union(a, b):
  '''
  return the union of two lists
  '''
  return list(set(a) | set(b))

def difference(a, b):
  '''
  show whats in list b which isnt in list a
  '''
  return list(set(b).difference(set(a)))