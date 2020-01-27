## Init properties
file="./application.properties"

if [ -f "$file" ]
then
  echo "$file found."

  while IFS='=' read -r key value # for each key/value
  do
    if [ ! -z "$key" ] # if key is not empty
    then
      echo "$key=$value"
      key=$(echo $key | tr '.' '_')
      export -p $key="$value" # export variable
    fi
  done < "$file"

else
  echo "$file not found."
fi