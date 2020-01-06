import multiprocessing

# listen to port 8080 on all available network interfaces
bind = '0.0.0.0:8080'

# Run the aiohttp app in multiple processes
workers = multiprocessing.cpu_count() * 2 + 1

# Use the correct worker class for aiohttp - this will change is using a different framework
worker_class = 'aiohttp.GunicornUVLoopWebWorker'
