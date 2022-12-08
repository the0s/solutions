# Given an array with number of gas stations
# following with a gas station gas amount with a value to spent to go there
# find if there is  way you can visit all the gas stations before you run out
# gas and return the gas station you start with

def gas_station_visits(str_arr):
	# code goes here
	gasStations = int(str_arr[0])

	for cnt in range(1,gasStations+1):
		gas = 0
		for i in range(gasStations):
			loc = i + cnt
			loc = loc % (gasStations) if loc > gasStations else loc
			gc = str_arr[loc].split(":")
			fill = int(gc[0])
			spend = int(gc[1])
			gas += fill
			gas -= spend
			if gas < 0:
				break
		#
		if gas >= 0:
			return cnt
	#
	return "impossible"

if __name__ == "__main__":
	print(gas_station_visits(["4","5:3","2:3","6:4","3:3"]))
