n=0 
while [ $n -le 100 ]; do 
    h=0 
    while [ $h -le $n ]; do
	h2=`expr $n - $h`
	rn=`./reg.py $n 2`
	rh1=`./reg.py $h 2`
	rh2=`./reg.py $h2 2`

	# echo $n $h `echo "l($rh1 + $rh2) - l($rn)" | bc -l`
	echo `echo $h/$n | bc -l` `echo "l($rh1 + $rh2) - l($rn)" | bc -l`
	
	let h+=1
    done 
    echo 
    let n+=1
done
