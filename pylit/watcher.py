import os, time
import pathlib
import pylit

pylit.defaults.code_block_marker = '.. code-block:: python'
pylit.defaults.comment_string = "# "
pylit.defaults.codeindent = 4
pylit.defaults.text_extensions = [".rst"]

def pylit_render(src, dst):
    try:
        pylit.main([src, dst])
    except IOError:
        pass

def create_missing_dirs(dst):
    dst_dir = os.path.dirname(dst)
    if not os.path.exists(dst_dir):
        p = pathlib.Path(dst_dir)
        p.mkdir(parents=True)

def render(filepath):
    # render the two way files
    src = filepath
    if filepath.endswith('py'):
        dst = f"{src.replace('/src/', '/docs/rst/')}.rst"        
    else:
        dst = src.replace('/docs/rst/', '/src/')[:-4]
        html_dst = src.replace('/rst/', '/html/')[:-4] + '.html'
        create_missing_dirs(html_dst)
        os.system(f'rst2html.py --stylesheet ./pylit/style.css {src} {html_dst}')
    
    # in order to brake the infinite loop in which the 
    # automatic modifications trigger other modifications
    # we wait for a reasonable human intervention time
    try:
        srctime = os.stat(src).st_mtime
        dsttime = os.stat(dst).st_mtime
        timedifference = round(srctime - dsttime)
        if timedifference > 2:
            pylit_render(src, dst)
    except FileNotFoundError as err:
        create_missing_dirs(dst)
        pylit_render(src, dst)

def get_files_stats(tracked_list):
    results = {}
    for f in tracked_list:
        results[f] = os.stat(f).st_mtime_ns
    return results

def check_index(index_mtime):
    # if index was modified, re-render it
    indextime = os.stat('./docs/rst/index.rst').st_mtime
    if indextime != index_mtime:
        os.system('rst2html.py --stylesheet ./pylit/style.css ./docs/rst/index.rst ./docs/html/index.html')
        index_mtime = indextime


def find_modified_files(found_files_stats, tracked_files_dict):
    modified_files = []
    for k, v in found_files_stats.items():
        if k not in tracked_files_dict:
            modified_files.append(k)
        else:
            if v != tracked_files_dict[k]:
                modified_files.append(k)

    return modified_files

def tracker(path_to_watch, tracked_files_dict, ext):
    found_files = []
    for root, dirs, files in os.walk(path_to_watch):
        for file in files:
            if file.endswith(ext):
                found_files.append((os.path.join(root, file)))
    # get all the stats of found files
    found_files_stats = get_files_stats(found_files)

    # select only the modified files
    modified_files = find_modified_files(found_files_stats, tracked_files_dict)

    for f in modified_files:
        render(f)

    return found_files_stats

py_path_to_watch = "./src"
rst_path_to_watch = "./docs/rst"
tracked_py_files = {}
tracked_rst_files = {}
index_mtime = None

print("I'm watching your back.. go on..")
while True:
    # find all py files
    tracked_py_files = tracker(py_path_to_watch, tracked_py_files, 'py')
    tracked_rst_files = tracker(rst_path_to_watch, tracked_rst_files, 'py.rst')
    check_index(index_mtime)
    time.sleep(2)