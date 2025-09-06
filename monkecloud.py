# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 03:38:11 2025

@author: steve
"""

# from google.cloud import storage

blob_folder_name="monkebot/savedata/"
local_folder_name="savedata/"

def download_all(): 
    # This will download the contents of the cloud "savedata" folder
    # into the local "savedata" folder.
    # NOTE: it does not delete files that don't exist on the cloud,
    # to avoid accidental deletion of files.
    # TL;DR only use this method to dowload files that exist in both locations.
    
    # Returns TRUE if the operation was successful
    return True
    
def upload_all():
    # This will upload all files in the local "savedata" folder
    # into the cloud "savedata" folder.
    # NOTE: it does not upload files that don't already exist on the cloud,
    # to avoid superfluously writing files that don't need to be saved
    # (plus I'm too lazy to have it creating new files on the cloud on the fly),
    # nor will it delete files that are on the cloud but not in the local folder
    # to avoid accidental deletion of files.
    # TL;DR only use this method to upload files that exist in both locations.
    
    # Returns TRUE if the operation was successful
    """
    try:
        storage_client = storage.Client(project="stevethecowbots")
        bucket = storage_client.bucket("stevethecowbots")
        blobs = storage_client.list_blobs(bucket)
        for blob in blobs:
            if blob.name.startswith(blob_folder_name) and not blob.name.endswith("/"):
                blob.upload_from_filename(local_folder_name + blob.name[len(blob_folder_name):])
        return True
    except:
        return False
    """        
    return True
            
def upload_file(filename):
    # Uploads a specific file. 
    # Filename should match path within the local "savedata" folder,
    # which has a corrosponding file in the cloud "savedata" folder.
    
    # Returns TRUE if the operation was successful
    return True
    
    
            


            
            