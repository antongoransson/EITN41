function cms_verify_mail {
  echo "----------Mail $1----------"
  openssl cms -decrypt -in $2.msg -recip $3.pem -inkey $4.pem -out $2.txt
  sed "3q;d" $2.txt
  openssl cms -digest_verify -in $2.txt 2> $2.verify | sed "3q;d"
  sed '1q;d' $2.verify
  echo
  rm $2.txt
}

mail1="inputs/B2/mail1"
mail2="inputs/B2/mail2"
mail3="inputs/B2/mail3"
cert="inputs/B2/certreceiver"
key="inputs/B2/keyreceiver"

cms_verify_mail 1 $mail1 $cert $key
cms_verify_mail 2 $mail2 $cert $key
cms_verify_mail 3 $mail3 $cert $key
