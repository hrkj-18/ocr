
#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
	if [ ! -z "$line" -a "$line" != " " ]; then
        printf "$line,">> $2
	fi
	
done < "$1"
printf "\n">>$2