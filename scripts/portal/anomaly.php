<html>
	<head>
 		<title>PHP Test</title>
 		
	</head>



	<body>
		<h1><center>A Study of Onions Price Fluctuations</center></h1>
		
 		<?php
 		$city = $_GET["city"];
 		$anomaly_id = $_GET["id"];
		$servername = "localhost";
		$username = "root";
		$password = "praneet";
		$database = "onion_analysis";

		// Create connection
		$conn = new mysqli($servername, $username, $password, $database);

		// Check connection
		if ($conn->connect_error) {
		    die("Connection failed: " . $conn->connect_error);
		} 
		if($city == "Mumbai") {
			$sql = "SELECT start_date, end_date, category FROM anomalies_mumbai WHERE id = ".$anomaly_id;
			$result = $conn->query($sql);
			
			$anomaly_row = $result->fetch_assoc();
			
			$retail_price_query = "SELECT * FROM retail_mumbai WHERE date >=DATE('".$anomaly_row["start_date"]."') and date <=DATE('".$anomaly_row["end_date"]."');";
			$retail_price_list = $conn->query($retail_price_query);
			
			$mandi_price_query = "SELECT * FROM mandiprice_mumbai WHERE date >=DATE('".$anomaly_row["start_date"]."') and date <=DATE('".$anomaly_row["end_date"]."');";
			$mandi_price_list = $conn->query($mandi_price_query);
			
			$mandi_arrival_query = "SELECT * FROM mandiarrival_mumbai WHERE date >=DATE('".$anomaly_row["start_date"]."') and date <=DATE('".$anomaly_row["end_date"]."');";
			$mandi_arrival_list = $conn->query($mandi_arrival_query);
			
		}
		elseif ($city == "Delhi") {
			$sql = "SELECT start_date, end_date, category FROM anomalies_delhi WHERE id = ".$anomaly_id;
			$result = $conn->query($sql);
			
			$anomaly_row = $result->fetch_assoc();
			
			$retail_price_query = "SELECT * FROM retail_delhi WHERE date >=DATE('".$anomaly_row["start_date"]."') and date <=DATE('".$anomaly_row["end_date"]."');";
			$retail_price_list = $conn->query($retail_price_query);
			
			$mandi_price_query = "SELECT * FROM mandiprice_delhi WHERE date >=DATE('".$anomaly_row["start_date"]."') and date <=DATE('".$anomaly_row["end_date"]."');";
			$mandi_price_list = $conn->query($mandi_price_query);
			
			$mandi_arrival_query = "SELECT * FROM mandiarrival_delhi WHERE date >=DATE('".$anomaly_row["start_date"]."') and date <=DATE('".$anomaly_row["end_date"]."');";
			$mandi_arrival_list = $conn->query($mandi_arrival_query);
		}
		elseif ($city == "Lucknow"){
			$sql = "SELECT start_date, end_date, category FROM anomalies_lucknow WHERE id = ".$anomaly_id;
			$result = $conn->query($sql);
			
			$anomaly_row = $result->fetch_assoc();
			
			$retail_price_query = "SELECT * FROM retail_lucknow WHERE date >=DATE('".$anomaly_row["start_date"]."') and date <=DATE('".$anomaly_row["end_date"]."');";
			$retail_price_list = $conn->query($retail_price_query);
			
			$mandi_price_query = "SELECT * FROM mandiprice_lucknow WHERE date >=DATE('".$anomaly_row["start_date"]."') and date <=DATE('".$anomaly_row["end_date"]."');";
			$mandi_price_list = $conn->query($mandi_price_query);
			
			$mandi_arrival_query = "SELECT * FROM mandiarrival_lucknow WHERE date >=DATE('".$anomaly_row["start_date"]."') and date <=DATE('".$anomaly_row["end_date"]."');";
			$mandi_arrival_list = $conn->query($mandi_arrival_query);
		}
		elseif ($city == "Bangalore"){
			$sql = "SELECT start_date, end_date, category FROM anomalies_bangalore WHERE id = ".$anomaly_id;
			$result = $conn->query($sql);
			
			$anomaly_row = $result->fetch_assoc();
			
			$retail_price_query = "SELECT * FROM retail_bangalore WHERE date >=DATE('".$anomaly_row["start_date"]."') and date <=DATE('".$anomaly_row["end_date"]."');";
			$retail_price_list = $conn->query($retail_price_query);
			
			$mandi_price_query = "SELECT * FROM mandiprice_bangalore WHERE date >=DATE('".$anomaly_row["start_date"]."') and date <=DATE('".$anomaly_row["end_date"]."');";
			$mandi_price_list = $conn->query($mandi_price_query);
			
			$mandi_arrival_query = "SELECT * FROM mandiarrival_bangalore WHERE date >=DATE('".$anomaly_row["start_date"]."') and date <=DATE('".$anomaly_row["end_date"]."');";
			$mandi_arrival_list = $conn->query($mandi_arrival_query);
		}

       	$i = 0;
    	while($row = $retail_price_list->fetch_assoc()) {
    		$dataPoints_retail[] = array("y" => $row["price"],"label"=>$i);
    		$i++;
    	}

    	$i = 0;
    	while($row = $mandi_price_list->fetch_assoc()) {
    		$dataPoints_mandiprice[] = array("y" => $row["price"],"label"=>$i);
    		$i++;
    	}

    	$i = 0;
    	while($row = $mandi_arrival_list->fetch_assoc()) {
   			$dataPoints_mandiarrival[] = array("y" => $row["arrival"],"label"=>$i);
    		$i++;
    	}
		
		if($anomaly_row["category"] == 2)
		{
			echo "<h2><center>Weather Anomaly</center></h2>";
		}
		elseif($anomaly_row["category"] == 5)
		{
			echo "<h2><center>Hoarding Anomaly</center></h2>";
		}
		elseif($anomaly_row["category"] == 8)
		{
			echo "<h2><center>Normal Period</center></h2>";
		}
		else
		{
			echo "<h2><center>Other</center></h2>";
		}
		echo "<h3><center>".$anomaly_row["start_date"]." - ".$anomaly_row["end_date"]."</center></h3>";
		echo $anomaly_table;
		echo "Connected successfully-".$city;
	
		?>
		<script>
			window.onload = function () {
 
			var chart = new CanvasJS.Chart("RetailPricechart", {
				title: {
					text: "Retail Price during the event"
				},
				axisY: {
					title: "Retail Price (Rs per quintal)",
					includeZero: false
				},
				axisX: {
					title: "Days"
				},
				data: [{
					type: "line",
					dataPoints: <?php echo json_encode($dataPoints_retail, JSON_NUMERIC_CHECK); ?>
				}]
			});
			chart.render();

			var chart2 = new CanvasJS.Chart("MandiPricechart", {
				title: {
					text: "Mandi Price during the event"
				},
				axisY: {
					title: "Mandi Price (Rs per quintal)",
					includeZero: false
				},
				axisX: {
					title: "Days"
				},
				data: [{
					type: "line",
					dataPoints: <?php echo json_encode($dataPoints_mandiprice, JSON_NUMERIC_CHECK); ?>
				}]
			});	
			chart2.render();

			var chart3 = new CanvasJS.Chart("MandiArrivalchart", {
				title: {
					text: "Mandi Arrival during the event"
				},
				axisY: {
					title: "Mandi Arrival"
				},
				axisX: {
					title: "Days"
				},
				data: [{
					type: "line",
					dataPoints: <?php echo json_encode($dataPoints_mandiarrival, JSON_NUMERIC_CHECK); ?>
				}]
			});
			chart3.render();
 
			}
		</script>

		<center><div id="RetailPricechart" style="height: 370px; width: 50%;"></div></center>
		<center><div id="MandiPricechart" style="height: 370px; width: 50%;"></div></center>
		<center><div id="MandiArrivalchart" style="height: 370px; width: 50%;"></div></center>
		<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
	</body>
</html>

