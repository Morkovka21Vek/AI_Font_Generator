import os
import shutil

def createFolders(flag=False):
    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.exists(os.path.join(directory, 'models')):
        os.makedirs(os.path.join(directory, 'models'))
        
    if not os.path.exists(os.path.join(directory, 'output', 'svg')):
        os.makedirs(os.path.join(directory, 'output', 'svg'))
        
    if flag:
        if not os.path.exists(os.path.join(directory, 'training', 'logs')):
            os.makedirs(os.path.join(directory, 'training', 'logs'))

        # if not os.path.exists(os.path.join(directory, 'training', 'trainingFonts')):
        #     os.makedirs(os.path.join(directory, 'training', 'trainingFonts'))
            
        if not os.path.exists(os.path.join(directory, 'training', 'trainingDataset')):
            os.makedirs(os.path.join(directory, 'training', 'trainingDataset'))
            
        if not os.path.exists(os.path.join(directory, 'training', 'trainingDatasetArray')):
            os.makedirs(os.path.join(directory, 'training', 'trainingDatasetArray'))

if __name__ == "__main__":
    createFolders(True)
else:
    createFolders(False)
