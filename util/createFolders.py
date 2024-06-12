import os
directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists(os.path.join(directory, 'models')):
    os.makedirs(os.path.join(directory, 'models'))
