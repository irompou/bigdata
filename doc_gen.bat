@ECHO OFF

call pandoc -f markdown_github -t docx -o doc\Readme.docx README.md
call pandoc -f markdown_github -t latex -o doc\Readme.pdf README.md
