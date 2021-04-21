rm -rf ./.parser_output
mkdir -p .parser_output/dataset

numberOfFiles=0

averageScore=0

for file in dataset/*.txt; do
	newname=${file%.*}
	python ../../main.py $file > .parser_output/$newname.json
	numberOfFiles=$(($numberOfFiles+1))
done

echo "Parsed files:" $numberOfFiles

for file in dataset/*.txt; do
	newname=${file%.*}
	
	res=$(python output_compare.py $newname.json .parser_output/$newname.json 2> /dev/null)
	echo $newname".json => " $res
	averageScore=$((averageScore+res))
	numberOfFiles=$(($numberOfFiles+1))
done

averageScore=$(echo $averageScore/50 | bc)
echo $averageScore
exit 0

