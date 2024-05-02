# views.py
import os
import shutil
from django.http import HttpResponse
from pywebcopy import save_website
import tempfile


def download_website(request):
    # Temporary directory to save the website
    temp_dir = tempfile.mkdtemp()

    try:
        # Download the website
        save_website(
            url="https://httpbin.org/",
            project_folder=temp_dir,
            project_name="my_site",
            bypass_robots=True,
            debug=True,
            open_in_browser=False,
            threaded=False,
        )

        # Compress downloaded files into a zip archive
        shutil.make_archive(os.path.join(temp_dir, "my_site"), "zip", temp_dir, "my_site")

        # Open the zip file and serve it as a response
        zip_file_path = os.path.join(temp_dir, "my_site.zip")
        with open(zip_file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/zip")
            response["Content-Disposition"] = 'attachment; filename="my_site.zip"'
            return response
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)