"""
初始化 Django 环境
Calling django.setup() is required for “standalone” Django usage
"""

import sys
import os
import django



# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

print(f'django_version={django.get_version()}')



    


if __name__ == '__main__':
    ...    

