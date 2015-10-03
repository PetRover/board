folderName=`date +%d-%b-%Y_%H-%M-%S`
folderName="backups/$folderName"

mkdir $folderName
echo ".$folderName"
find . -type f -name '*.*#*' -maxdepth 1 -print0 | xargs -0 -J % mv % "./$folderName"
find . -name '*.gpi' -delete
find . -name '*.dri' -delete
rm -rf gerbers/
mkdir gerbers
find . -type f -name '*.ger' -maxdepth 1 -print0 | xargs -0 -J % mv % "gerbers"
find . -type f -name '*.xln' -maxdepth 1 -print0 | xargs -0 -J % mv % "gerbers"
zip -r gerbers.zip gerbers


