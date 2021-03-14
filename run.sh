#! /usr/bin/env sh
source yieldfarmEnv/bin/activate
dateNow=$(date +'%Y%m%dT%H%M%S')

echo "--- Date: $dateNow"

# Checkout data branch
git checkout data >/dev/null
python src/dataUpdate.py -v

if [[ $? -eq 0 ]]; then
	tail -n 1 run.log >> numbers.log
	echo "Finished successfully! Committing data!"
	git add run.log numbers.log data 2> /dev/null
	git commit -m "update: Data update on $dateNow"
	git push origin data
fi
echo "---------------------------------------------------------"
