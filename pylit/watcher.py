import os, time
import pylit

pylit.defaults.code_block_marker = '.. code-block:: python'
pylit.defaults.comment_string = "# "
pylit.defaults.codeindent = 4
pylit.defaults.text_extensions = [".rst"]

def render(filepath):
    # render the two way files
    src = filepath
    if filepath.endswith('py'):
        dst = f"{src.replace('/src/', '/docs/rst/')}.rst"        
    else:
        dst = src.replace('/docs/rst/', '/src/')[:-4]
        html_dst = src.replace('/rst/', '/html/')[:-4] + '.html'
        os.system(f'rst2html.py --stylesheet ./pylit/style.css {src} {html_dst}')
    
    # in order to brake the infinite loop in which the 
    # automatic modifications trigger other modifications
    # we wait for a reasonable human intervention time
    srctime = os.stat(src).st_mtime
    dsttime = os.stat(dst).st_mtime
    timedifference = abs(round(srctime - dsttime))
    if timedifference > 2:
        pylit.main([src, dst])

def get_files_stats(path_to_watch, endsw):
    results = []
    for f in os.listdir(path_to_watch):
        fp = f'{path_to_watch}/{f}'
        if f.endswith(endsw):
            results.append(
                (
                    os.stat(fp).st_mtime_ns,
                    f
                )
            )
    return results

def find_file_by_time(time, files):
    return next(filter(lambda x: x[0] == time, files))[1]

def tracker(path_to_watch, tracked_list, ext):
    # get all the stats of tracked files
    next_tracked_files = get_files_stats(path_to_watch, ext)
    # get only the actual times
    ntf_time = map(lambda x: x[0], next_tracked_files)
    # get the old times
    tf_time = map(lambda x: x[0], tracked_list)
    # select only the modified files
    refresh_files = [find_file_by_time(f, next_tracked_files) for f in ntf_time if not f in tf_time]

    for f in refresh_files:
        render(f'{path_to_watch}/{f}')

    return next_tracked_files

py_path_to_watch = "./src"
rst_path_to_watch = "./docs/rst"
tracked_py_files = []
tracked_rst_files = []

while True:
    time.sleep(2)
    tracked_py_files = tracker(py_path_to_watch, tracked_py_files, 'py')
    tracked_rst_files = tracker(rst_path_to_watch, tracked_rst_files, 'rst')