# Get the filepath for this script 
base="`dirname \"$0\"`"
#echo $base

# Get the relative path for the file to change
subdir="/../../date/ever_changing_date_file.txt"
#echo $subdir

# Compose the right path for the date file
new_path="$base$subdir"
#echo $new_path

# Get the current date and time
new_date=$(date +%Y-%m-%d,%H:%M:%S)
#echo $new_date

# Update the file
echo $new_date > $new_path
echo "Updated date for $GITHUB_REPOSITORY on $new_path to $new_date"