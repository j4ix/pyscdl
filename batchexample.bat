::  pyscdl v1.1
::
::  usage: catalogupdater.exe [-h] <cid> <url> [output_dir] [default_genre] [do_meta]
::
::  required arguments:
::    cid                client id
::    url                soundcloud user by url
::
::  optional arguments:
::    -h, --help         show this shit
::    output_dir         output directory
::    default_genre      default genre to use if none
::    do_meta            compute metadata for downloaded tracks
::
::  examples:
::    catalogupdater.exe Mx2TehYCr804EIo6LQ7OARjZpWjMdVOx j4ix . Dubstep True         -->  download to current directory with meta processing
::    catalogupdater.exe Mx2TehYCr804EIo6LQ7OARjZpWjMdVOx j4ix c:/users/j4ix/music    -->  download to music directory with meta processing

catalogupdater.exe Mx2TehYCr804EIo6LQ7OARjZpWjMdVOx j4ix .