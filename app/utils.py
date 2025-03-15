import os
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """Check if the filename has an allowed extension."""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_blob_storage(file):
    """Upload a file to Azure Blob Storage and return the URL."""
    if not file:
        return None
    
    if not allowed_file(file.filename):
        return None
    
    # Secure the filename to prevent any malicious filenames
    filename = secure_filename(file.filename)
    
    # Generate a unique filename using timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}_{filename}"
    
    account_name = current_app.config['STORAGE_ACCOUNT_NAME']
    account_key = current_app.config['STORAGE_ACCOUNT_KEY']
    container_name = current_app.config['STORAGE_CONTAINER_NAME']
    
    try:
        # Create a blob service client
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Get container client
        container_client = blob_service_client.get_container_client(container_name)
        
        # Create container if it doesn't exist
        if not container_client.exists():
            container_client.create_container(public_access="blob")
        
        # Get blob client and upload the file
        blob_client = container_client.get_blob_client(filename)
        blob_client.upload_blob(file)
        
        # Generate a URL for the blob
        blob_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{filename}"
        return blob_url
        
    except Exception as e:
        print(f"Error uploading to blob storage: {str(e)}")
        return None