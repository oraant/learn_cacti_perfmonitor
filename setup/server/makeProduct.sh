rm -rf bak/
rm -rf tmp/
rm -rf .git/

rm -rf datas/*
rm -rf dbm/*
rm -rf log/*

rm -f run.log
rm -f run.err
rm -f call.py

python crypto.py -d conf/getLinux.conf
python crypto.py -d conf/getOracle.conf
python crypto.py -d conf/getTbs_dg.conf
python crypto.py -d conf/getThreshold.conf
python crypto.py -d conf/verify.conf

python crypto.py -c dmAlert.py
python crypto.py -c dmCapture.py
python crypto.py -c dmHandler.py
python crypto.py -c sendmail.py
python crypto.py -c sendsms.py
python crypto.py -c widget.py

rm -f *.c
rm -f *.pyc
rm -f dmAlert.py dmCapture.py dmHandler.py sendmail.py sendsms.py widget.py

tar -zcf perfmonitor.tar.gz perfmonitor
