import os

list = os.listdir(os.path.dirname(__file__))
packages = []

# filter testcases
for item in list:
    if item.endswith('.py'):
        m = item.replace('.py', '')
        packages.append(m)

__all__ = packages
