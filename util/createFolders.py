import os
import shutil

directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists(os.path.join(directory, 'models')):
    os.makedirs(os.path.join(directory, 'models'))
    
if not os.path.exists(os.path.join(directory, 'output', 'svg')):
    os.makedirs(os.path.join(directory, 'output', 'svg'))
    
if True:
    shutil.rmtree(os.path.join(directory, 'cache'))
    
if not os.path.exists(os.path.join(directory, 'cache')):
    os.makedirs(os.path.join(directory, 'cache'))

if not os.path.exists(os.path.join(directory, 'cache', 'svgFont2img')):
    os.makedirs(os.path.join(directory, 'cache', 'svgFont2img'))
