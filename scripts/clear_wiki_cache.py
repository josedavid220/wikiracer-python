import os
import shutil

cache_dir = os.path.join(os.path.dirname(__file__), '../wiki_cache')
cache_dir = os.path.abspath(cache_dir)

if os.path.isdir(cache_dir):
    for filename in os.listdir(cache_dir):
        file_path = os.path.join(cache_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
else:
    print(f"Directory {cache_dir} does not exist.")