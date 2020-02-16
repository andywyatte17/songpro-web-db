# Converting SongPro databases on Linux

## My Linux

  * Linux Mint

## Install

    sudo apt install python3.4
    sudo apt-get install mdbtools   

## Mdb Tools

    mdb-tables file.spdb
    # Authors CatList Chorus...

    mdb-export file.spdb Chorus > chorus.csv
    python3 csv-to-json.py chorus.csv chorus.json




 
