
# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] 
  
## [1.0.6] - 2021-01-02
  
Installation see project description.
This is the first release. It is based on the project [Yandex Images Download](https://pypi.org/project/yandex-images-download/)
1.0.4 from Alexander Kozlov. 
 
### Added
- Existing images can be skipped.  
- Set search keywords as Lightroom keywords.
- Set image url as creator web address (IPTC)
### Changed
### Fixed
- Replaced request.path by request.url in get_response() module download.py.
 
## [1.0.7] - 2021-01-07
To update just run 
```pip install yandex2lightroom```

### Added
- Added wallpaper as additional image size (option --isize=wallpaper)
### Changed
### Fixed

## [1.0.8] - 2021-01-08
To update just run 
```pip install yandex2lightroom```

### Added
### Changed
### Fixed
- Option ``--num-workers`` did not work