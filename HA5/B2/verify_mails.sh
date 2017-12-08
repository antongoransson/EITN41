mail1="mail1"
mail2="mail2"
mail3="mail3"
certreceiver="certreceiver"
keyreceiver="keyreceiver"

echo 'Mail 1'
openssl cms -decrypt -in $mail1.msg -recip $certreceiver.pem -inkey $keyreceiver.pem -out $mail1.txt
openssl cms -digest_verify -in $mail1.txt
sed '3q;d' $mail1.txt
echo '------------------------------------------'

echo -e '\nMail 2'
openssl cms -decrypt -in $mail2.msg -recip $certreceiver.pem -inkey $keyreceiver.pem -out $mail2.txt
openssl cms -digest_verify -in $mail2.txt
sed '3q;d' $mail2.txt
echo '------------------------------------------'

echo -e '\nMail 3'
openssl cms -decrypt -in $mail3.msg -recip $certreceiver.pem -inkey $keyreceiver.pem -out $mail3.txt
openssl cms -digest_verify -in $mail3.txt
sed '3q;d' $mail3.txt
echo '------------------------------------------'


rm $mail1.txt
rm $mail2.txt
rm $mail3.txt
