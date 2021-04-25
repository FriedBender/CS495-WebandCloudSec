import time

def time_decorator(func):
  """
  Takes a function and returns a version of it that prints out the elapsed time for executing it
  :param func: Function to decorate
  :return: Function which outputs execution time
  :rtype: Function
  """
  def inner(*args, **kwargs):
      s = time.perf_counter()
      return_vals = func(*args, **kwargs)
      elapsed = time.perf_counter() - s
      print(f'Function returned: {return_vals}')
      return(elapsed)
  return(inner)
