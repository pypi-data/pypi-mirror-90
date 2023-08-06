# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['csfutils', 'csfutils.blob']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-storage>=1.35.0,<2.0.0']

setup_kwargs = {
    'name': 'csfutils',
    'version': '0.2.0',
    'description': 'Python utility for Cloud Storage for Firebase.',
    'long_description': '# cloud-storage-for-firebase-utils\n\n[![PyPI version](https://badge.fury.io/py/csfutils.svg)](https://badge.fury.io/py/csfutils) [![Python Versions](https://img.shields.io/pypi/pyversions/csfutils.svg)](https://pypi.org/project/csfutils/)\n![lint & test](https://github.com/quwac/cloud-storage-for-firebase-utils/workflows/lint%20&%20test/badge.svg) [![codecov](https://codecov.io/gh/quwac/cloud-storage-for-firebase-utils/branch/main/graph/badge.svg)](https://codecov.io/gh/quwac/cloud-storage-for-firebase-utils)\n\nPython utility for Cloud Storage for Firebase.\n\n## What is This?\n\nIn order to use [Google Cloud Storage](https://cloud.google.com/storage?hl=en) with the [Firebase](https://firebase.google.com/docs/storage?hl=en) framework, you have to:\n\n* Give an access token to uploaded files,\n* Publish a URL with an access token for the domain `firebasestorage.googleapis.com`.\n* As a further application, you may want to grant a new access token, remove an existing access token, or in a real use case, get a `google.cloud.storage.Blob` instance from a URL.\n\nUnfortunately [google-cloud-storage](https://pypi.org/project/google-cloud-storage/) package does not provide the functions for them.\n\nBut by using **cloud-storage-for-firebase-utils** you can easily achieve them👍.\n\n## Requirements\n\n* Python >= 3.6\n* [google-cloud-storage](https://pypi.org/project/google-cloud-storage/) >= 1.35.0\n\n## Quick Start\n\nFirst, install by `pip intall csfutils` .\nSecond, prepare a target file `stars⭐.jpg` .\nFinally, run below code❗\n\n```python\nfrom google.cloud.storage import Blob, Bucket, Client\n\n# Import package\n# ==============\nimport csfutils\n\n# Initialize google.cloud.storage.Client, Bucket and Blob instances\n# =================================================================\nstorage: Client = Client()\nbucket: Bucket = storage.bucket("example-project.appspot.com")  # PUT YOUR BUCKET NAME\nblob: Blob = bucket.blob("images/stars⭐.jpg")  # PUT PATH ON CLOUD STORAGE YOU WANT\n\n# 🔥Upload "./stars⭐.jpg" to Cloud Storage for Firebase\n# ======================================================\nuploaded_url: str = csfutils.upload_from_filename_for_firebase(blob, "./stars⭐.jpg")\nprint(f"uploaded_url={uploaded_url}")\n# --> uploaded_url=https://firebasestorage.googleapis.com/v0/b/example-project.appspot.com/o/images%2Fstars%E2%9C%A7.jpg?alt=media&token=f7d0815d-96f8-4907-b22c-70ad9e38d7ff\n\n# csfutils.upload_from_file_for_firebase() and csfutils.upload_from_string_for_firebase() also exist.\n\n# 🔥Add, get and delete an access token\n# =====================================\ncurrent_access_token = csfutils.get_access_token(blob)\nassert type(current_access_token) is str\nprint(f"current_access_token={current_access_token}")\n# --> current_access_token=f7d0815d-96f8-4907-b22c-70ad9e38d7ff\n\nnew_access_token: str = csfutils.add_access_token(blob)\nprint(f"new_access_token={new_access_token}")\n# --> new_access_token=e0d97b72-44c3-415d-8d88-1e3aeae2fc28\n\naccess_tokens = csfutils.get_access_token(blob)\nassert isinstance(access_tokens, list)\nprint(f"access_tokens={access_tokens}")\n# --> current_access_token=[\'f7d0815d-96f8-4907-b22c-70ad9e38d7ff\',\'e0d97b72-44c3-415d-8d88-1e3aeae2fc28\']\n\ncsfutils.delete_access_token(blob, new_access_token)\nprint(f"latest_access_token={csfutils.get_access_token(blob)}")\n# --> latest_access_token=f7d0815d-96f8-4907-b22c-70ad9e38d7ff\n\n# 🔥Get google.cloud.storage.Blob instance from URL\n# =================================================\nblob_ref_from_url: Blob = csfutils.ref_from_url(\n    storage,\n    "https://firebasestorage.googleapis.com/v0/b/example-project.appspot.com/o/images%2Fstars%E2%9C%A7.jpg?alt=media&token=f7d0815d-96f8-4907-b22c-70ad9e38d7ff"\n)\n# --> blob_ref_from_url == storage.bucket("example-project.appspot.com").get_blob("images/stars✧.jpg")\n\n```\n\n## Bonus Track\n\n```python\nfrom csfutils\n\n# BONUS 1: Get google.cloud.storage.Client instance\n# =================================================\nstorage: Client = csfutils.init_storage("./your_service_account.json")\n\n# BONUS 2: Parse URL to bucket name & path\n# ========================================\nbucket_name, path = csfutils.parse_url("https://firebasestorage.googleapis.com/v0/b/example-project.appspot.com/o/images%2Fstars%E2%9C%A7.jpg?alt=media&token=f7d0815d-96f8-4907-b22c-70ad9e38d7ff")\nprint(f"bucket_name={bucket_name},path={path}")\n# --> bucket_name=example-project.appspot.com,path=images/stars⭐.jpg\n\n# BONUS 3: Get 3 URLs: firebasestorage.googleapis.com, storage.googleapis.com and storage.cloud.google.com\n# ========================================================================================================\nblob: Blob = storage.bucket(bucket_name).blob(path)\n\nfirestorage_url = csfutils.get_download_url(blob)\nprint(f"firestorage_url={firestorage_url}")\n# --> firestorage_url=https://firebasestorage.googleapis.com/v0/b/example-project.appspot.com/o/images%2Fstars%E2%9C%A7.jpg?alt=media&token=f7d0815d-96f8-4907-b22c-70ad9e38d7ff\n\npublic_url = csfutils.get_download_url(blob, csfutils.UrlType.PUBLIC_URL)\nprint(f"public_url={public_url}")\n# --> firestorage_url=https://storage.googleapis.com/example-project.appspot.com/images/stars%E2%9C%A7.jpg\n\nauthenticated_url = csfutils.get_download_url(blob, csfutils.UrlType.AUTHENTICATED_URL)\nprint(f"authenticated_url={authenticated_url}")\n# --> authenticated_url=https://storage.cloud.google.com/example-project.appspot.com/images/stars%E2%9C%A7.jpg\n\n# BONUS 4: Get GS path\n# ====================\ngs_path = csfutils.get_gs_path(blob)\nprint(f"gs_path={gs_path}")\n# --> gs_path=gs://example-project.appspot.com/images/stars⭐.jpg\n\n```\n\n## License\n\nMIT License\n',
    'author': 'quwac',
    'author_email': '53551867+quwac@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quwac/cloud-storage-for-firebase-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
