report_branch="branch="$(git branch --show-current)
ress="value="$(bash test.sh | tail -n1)


ak="apiKey="$1


curl -L -X post --data $report_branch --data $ress --data $ak https://script.google.com/macros/s/AKfycbw8fgrCkrLpDNteVDMwt6S0s-sqBDQdScSV0buOPqfhDepM1AtkI4OB6yCL5wjeagxL/exec

