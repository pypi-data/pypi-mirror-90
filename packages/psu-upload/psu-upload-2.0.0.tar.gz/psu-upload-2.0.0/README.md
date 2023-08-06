# PSU-Upload
Reusable Django app specifically for PSU's custom-built web applications.  
Provides the ability to upload files in any site using the psu_base plugin.  

## Quick Start

### Dependencies
The following dependency is REQUIRED and must be installed in your app:
- [psu-base](https://pypi.org/project/psu-base/)

### Installation
```shell script
pip install psu-upload
```

### Configuration
1. Configure [psu-base](https://pypi.org/project/psu-base/) in your Django app
1. Add `psu-upload` to your `requirements.txt`
1. Add both PSU-Upload and storages to your INSTALLED_APPS in `settings.py`:
    ```python
    INSTALLED_APPS = [
       ...
       'psu_base',
       'psu_upload',
       'storages',  # Only required if saving files in Amazon S3
    ]
    ```
1. Configure your app's top-level `urls.py` to include Upload views:  
*Note: As-of version 1.0.0, no useful URLs exist, but may be added in future versions*
    ```python
    urlpatterns = [
        ...
        path('upload/', include(('psu_upload.urls', 'psu_upload'), namespace='upload')),
    ]
   
## Additional Configuration for Storage in S3
*If you're not using Amazon S3, these steps are not required*
   
1. Add the following settings to `settings.py`:  
    ```python
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = '<Your App Name>.wdt.pdx.edu'
    AWS_S3_ENDPOINT_URL = "https://s3-us-west-2.amazonaws.com/<Your App Name>.wdt.pdx.edu"
    AWS_DEFAULT_REGION = "us-west-2"
    AWS_S3_REGION_NAME = "us-west-2"
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    ``` 
1. Add the following settings to `local_settings.py`:
    ```python
    AWS_ACCESS_KEY_ID = '<Put this in local_settings.py>'
    AWS_SECRET_ACCESS_KEY = '<Put this in local_settings.py>'
    ``` 
1. In the `if_aws` condition of `settings.py` add this:
    ```python
        # File Upload Settings
        AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
    ```

## Usage

### Limiting file types accepted
By default, only office-type docs will be accepted (pdf, jpg, text, ms-office).
You can specify accepted file types in `settings.py` with `ALLOWED_UPLOAD_TYPES = [...]`  
The list of allowed types may include any or all of:
 1. file extensions (['pdf', '.txt', ...]), which will automatically be converted to MIME types for you
 1. actual MIME types (['text/plain'])
 1. defined groups of doc types (['office', 'image'])
 
Validation will automatically be done for you based on MIME type (not just the file extension)

### Upload one or more files from a single input
*Use this function:*
```
upload_service.upload_files(request, input_name, sequenced_filename=None, parent_directory=None):
    """
    Action for saving one or more uploaded file
    Parameters:
        request - The Django request object
        input_name - The name of the file input in your HTML form
        sequenced_filename  - Gives all files the same name with a sequence number appended
                            - Retain original filename if not specified
        parent_directory - The directory (within your app directory) the files will live in on AWS/S3
    """
```
*Steps:*
1. Make sure your form tag has `method="post"` and `enctype="multipart/form-data"`
1. Make sure your file input tag has `multiple="multiple"`
1. In your view:
```python
from psu_upload.services import upload_service

def my_view(request):
        
    # Keep original file name (S3 will append junk to it if the name is already taken)
    uploaded_files = upload_service.upload_files(request, '<file_input_name>')

    # ... OR ...

    # Specify a new file name (will append sequence numbers for multiple files)
    uploaded_files = upload_service.upload_files(
        request, '<file_input_name>',
        sequenced_filename='example-', 
        parent_directory='examples'
    )
```

### Upload a single file (multiples not allowed)
*Use this function:*
```
upload_service.upload_file(file_instance, specified_filename=None, parent_directory=None):
    """
    Action for saving ONE uploaded file
    Parameters:
        file_instance - The in-memory file to be saved (from request.FILES)
        specified_filename  - Rename the file (automatically retains the original extension)
                            - Retains the original filename if not specified
        parent_directory - The directory (within your app directory) the file will live in on AWS/S3
    """
```
1. Make sure your form tag has `method="post"` and `enctype="multipart/form-data"`
1. In your view:
```python
from psu_upload.services import upload_service

def my_view(request):
    if request.method == 'POST':
        # Keep original file name
        uploaded_file = upload_service.upload_file(request.FILES['<file_input_name>'])
    
        # ... OR ...

        # Specify a new file name (retains the original extension)
        # Specify a parent directory in S3
        uploaded_file = upload_service.upload_file(
            request.FILES['<file_input_name>'], 
            specified_filename='my_new_filename', 
            parent_directory='all_files/my_files/important-files'
        )
```

### Read files without saving them anywhere
*Use these functions:*
```
# For a single file
upload_service.read_uploaded_file(request, input_name, byte_limit=500000, convert_to_string=True):
    """
    Return the contents of an uploaded file without actually saving it anywhere
    """

# For multiple files
upload_service.read_uploaded_files(request, input_name, byte_limit=500000, convert_to_string=True):
    """
        Return the contents of uploaded files without actually saving them anywhere
        Returns a dict with the file name as the key, and contents as the value
    """
```

### Template Tags

#### Print a link to a file:
```
{% load upload_taglib %}

{%file_link file=file_instance%}

Examples of optional attrs:
{%file_link file=file_instance size=True %}  <!-- Show file size -->
{%file_link file=file_instance icon='fa fa-star' %}  <!-- specify file icon -->
{%file_link file=file_instance icon=False %}  <!-- no file icon -->
```
See the code for available attrs.  Any unexpected attrs (id, style, etc) will be included in the <span> wrapper.

#### Display a DatabaseFile in an <img /> tag
*This probably won't work for S3 files, but hasn't been tried yet*
```
{% load upload_taglib %}

{%database_image file=file_instance %}

Any attrs that can appear in an <img /> tag can also be provided.
```

## For Developers
The version number must be updated for every PyPi release.
The version number is in `psu_upload/__init__.py`

### Document Changes
Record every change in [docs/CHANGELOG.txt](docs/CHANGELOG.txt)

### Publishing to PyPi
1. Create accounts on [PyPi](https://pypi.org/account/register/) and [Test PyPi](https://test.pypi.org/account/register/)
1. Create `~/.pypirc`
    ```
    [distutils]
    index-servers=
        pypi
        testpypi
    
    [testpypi]
    repository: https://test.pypi.org/legacy/
    username: mikegostomski
    password: pa$$w0rd
    
    [pypi]
    username: mikegostomski
    password: pa$$w0rd
    ```
1. Ask an existing developer to add you as a collaborator - [test](https://test.pypi.org/manage/project/psu-upload/collaboration/) and/or [prod](https://pypi.org/manage/project/psu-upload/collaboration/)
1. `python setup.py sdist bdist_wheel --universal`
1. `twine upload --repository testpypi dist/*`
1. `twine upload dist/*`
1. Tag the release in Git.  Don't forget to push the tag!
Example:
```shell script
git tag 0.1.2
git push origin 0.1.2 
```