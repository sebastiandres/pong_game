# Path to date file
new_path="./date/ever_changing_date_file.txt"
echo $new_path

# Get the current date and time
new_date=$(date +%Y-%m-%d,%H:%M:%S)
#echo $new_date

# Update the file
echo $new_date > $new_path
echo "Updated date for $GITHUB_REPOSITORY on $new_path to $new_date"

# Check answer
cat $new_path