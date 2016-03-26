# repoeditor
Editor of small and medium size repositories of Npackd package manager.

## Usage
To start repoeditor simply double click repoeditor.py file, or go to console
and invoke:
```
repoeditor
```

## Notes
Your browser may not display XML file as expected until you copy `summary.xls`
file to the same directory where XML file is. `summary.xls` can be found in
`<repoeditor>/templates` directory. If you don't want to use such file, remove:

`<?xml-stylesheet type="text/xsl" href="summary.xsl"?>`

line in `<repoeditor>/templates/header.xml` and regenerate your XML file.
