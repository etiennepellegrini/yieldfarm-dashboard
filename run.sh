#! /usr/bin/env sh
source yieldfarmEnv/bin/activate
dateNow=$(date +'%Y%m%dT%H%M%S')

echo "--- Date: $dateNow"

# Checkout data branch
git checkout data >/dev/null
python src/dataUpdate.py -v > data/.tmp

if [[ $? -eq 0 ]]; then
	echo "Finished successfully! Committing data!"
	tail -n 1 data/.tmp >> data/summary.log
	git add data 2> /dev/null
	git commit -m "update: Data update on $dateNow"
	git push origin data
fi
echo "---------------------------------------------------------"
