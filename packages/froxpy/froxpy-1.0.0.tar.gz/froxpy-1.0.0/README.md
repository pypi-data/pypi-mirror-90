# froxpy
A python library to manage and test proxy lists

# Documentation

### froxpy.gen_proxy_dict(proxies)
Returns a dictionary object with the format the 'requests' library from python needs to use proxies in requests.

### froxpy.test_proxies(proxies, timeout, output)
Return a tuple with three lists:
  - 0: is the list with working proxies
  - 1: is the list with bad proxies (caused by an error)
  - 2: is the list with timeout proxies (cause by the timeout)
  
Defaults:
  - 'proxies': is a empty list as default
  - 'timeout': is set to 15 seconds as default
  - 'output': is set to False as default
