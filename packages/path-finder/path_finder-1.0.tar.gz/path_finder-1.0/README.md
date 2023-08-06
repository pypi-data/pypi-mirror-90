## path_finder

### Description
An interface for finding directories and files by combining best of both worlds: glob/rglob (speed) and regex (flexibility).

### Features
path_finder officially supports Python 3.5–3.8. \
The two main features are: path_finder.DirFinder and path_finder.FileFinder (see Usage) 

### License 
[MIT][mit]

### Releases
[PyPi][pypi]

### Contributions
All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.
Issues are posted on: https://github.com/hdsr-mid/path_finder/issues

[pypi]: https://pypi.org/project/path-finder/
[mit]: https://github.com/hdsr-mid/path_finder/blob/main/LICENSE.txt


### Usage
#### Test path_finder
```
> cd path_finder
> pytest
```

#### Example FileFinder:
```
from pathlib import Path
import path_finder

start_dir1          = pathlib.Path('start_search_from_this_dir')
start_dir2          = pathlib.Path('and_start_search_from_this_dir')
limit_depth         = True
depth               = 2  # 2, so search in start_dir1, subdir and subsubdirs (same for start_dir2) 
filename_regex      = '^[0-9]{8}_blabla'
extension           = '.csv'  # choose from ('.jpg', '.png', '.txt', '.xml', '.csv', '.xlsx', '.pdf', '.h5', '.nc', '.zip')   

file_finder = path_finder.FileFinder(
    multi_start_dir=[start_dir1, start_dir2],
    extension=extension,
    limit_depth=True,                   
    depth=depth,
    filename_regex=filename_regex
)
                    
paths = file_finder.paths  # returns a List[Path]
paths_empty_files = file_finder.paths_empty_file  # returns a List[Path]
```


#### Example DirFinder:
```
from pathlib import Path
import path_finder

dir_finder = path_finder.DirFinder(
    single_start_dir=pathlib.Path('start_search_from_this_dir')
    exclude_empty_dirs=True,
    limit_depth=True,
    depth=0,  # so only search in single_start_dir
)

paths = dir_finder.paths  # returns a List[Path]
paths_empty_files = dir_finder.paths_empty_file  # returns a List[Path]
```
