<html>
	<head>
 		<title>PHP Test</title>
 		<style>
			table {
			    font-family: arial, sans-serif;
			    border-collapse: collapse;
			    width: 100%;
			}

			td, th {
			    border: 1px solid #dddddd;
			    text-align: left;
			    padding: 8px;
			}

			tr:nth-child(even) {
			    background-color: #dddddd;
			}
		</style>
	</head>
	<body>
		<h1><center>A Study of Onions Price Fluctuations</center></h1>
		
 		<?php
 		$city = $_GET["city"];
		$servername = "localhost";
		$username = "root";
		$password = "praneet";
		$database = "onion_analysis";
		$cate = $_GET["cate"];
		// Create connection
		$conn = new mysqli($servername, $username, $password, $database);

		// Check connection
		if ($conn->connect_error) {
		    die("Connection failed: " . $conn->connect_error);
		} 
		if($city == "Mumbai") {

			$sql = "SELECT anomalies_mumbai.id, start_date, end_date, category, link FROM anomalies_mumbai,mumbai_newspaper where anomalies_mumbai.id = mumbai_newspaper.id";
			$sql2 = "SELECT label from semi_labels_mumbai";
		}
		elseif ($city == "Delhi") {
			
			$sql = "SELECT anomalies_delhi.id, start_date, end_date, category, link FROM anomalies_delhi,delhi_newspaper where anomalies_delhi.id = delhi_newspaper.id";	
			$sql2 = "SELECT label from semi_labels_delhi";
		
		}
		elseif ($city == "Lucknow"){
			
			$sql = "SELECT anomalies_lucknow.id, start_date, end_date, category, link FROM anomalies_lucknow,lucknow_newspaper where anomalies_lucknow.id = lucknow_newspaper.id";
			$sql2 = "SELECT label from semi_labels_lucknow";
		
		}
		elseif ($city == "Bangalore"){
			$sql = "SELECT anomalies_bangalore.id, start_date, end_date, category, link FROM anomalies_bangalore,bangalore_newspaper where anomalies_bangalore.id = bangalore_newspaper.id";
			// $sql2 = "SELECT label from semi_labels_bangalore";
		
		}
		$result = $conn->query($sql);

		// $result2 = $conn->query($sql2);

		if ($result->num_rows > 0) {
    		// output data of each row
			$anomaly_table = "<table style=\"width:100%\">
			<tr>
				<th>Sr.No.</th>
				<th>Start Date</th>
				<th>Last Date</th>
				<th>Category</th>
				<th>Link</th>
			<tr>";

    		while($row = $result->fetch_assoc()) {
    			if($cate == "All")
    			{
    				if($row["category"] == 2 or $row["category"] == 5 or $row["category"] == 8){
        		$anomaly_table = $anomaly_table."<tr><th><a href=\"/anomaly.php?city=".$city."&id=".$row["id"]."\">".$row["id"]."</a></th><th>".$row["start_date"]. "</th><th>" . $row["end_date"]. "</th><th>" . $row["category"]. "</th><th><a href=\"".$row[link]."\">".$row["link"]."</a></th></tr>";
    				}
    			}
    			elseif($cate == "Hoarding")
    			{
    				if($row["category"] == 5){
        		$anomaly_table = $anomaly_table."<tr><th><a href=\"/anomaly.php?city=".$city."&id=".$row["id"]."\">".$row["id"]."</a></th><th>".$row["start_date"]. "</th><th>" . $row["end_date"]. "</th><th>Hoarding</th><th><a href=\"".$row[link]."\">".$row["link"]."</a></th></tr>";
    				}
    			}
    			elseif($cate == "Weather")
    			{
    				if($row["category"] == 2){
        		$anomaly_table = $anomaly_table."<tr><th><a href=\"/anomaly.php?city=".$city."&id=".$row["id"]."\">".$row["id"]."</a></th><th>".$row["start_date"]. "</th><th>" . $row["end_date"]. "</th><th>Weather</th><th><a href=\"".$row[link]."\">".$row["link"]."</a></th></tr>";
    				}
    			}
    			elseif($cate == "Normal")
    			{
    				if($row["category"] == 8){
        		$anomaly_table = $anomaly_table."<tr><th><a href=\"/anomaly.php?city=".$city."&id=".$row["id"]."\">".$row["id"]."</a></th><th>".$row["start_date"]. "</th><th>" . $row["end_date"]. "</th><th>" . $row["category"]."</th><th>".$row["link"]."</th></tr>";
    				}
    			}
    		}
    		$anomaly_table=$anomaly_table."</table>";
    	}
		else {
    		echo "0 results";
		}
		echo "<h2><center>Anomalies observed in ".$city."</center></h2>";
		echo "<h3><center>2=Weather, 5=Hoarding, 8=Normal</center></h3>";
		echo "<center>
    		<form action=\"base.php\">
    		  <fieldset> 
    		    Anomalies:
    		    <select name=\"cate\">
    		      <option value=\"All\">All</option>
    		      <option value=\"Hoarding\">Hoarding</option>
    		      <option value=\"Weather\">Weather</option>
    		      <option value=\"Normal\">Normal</option>
    		    </select>
    		    <input type=\"hidden\" name=\"vegetable\" value=\"Onion\">
    		    <input type=\"hidden\" name=\"city\" value=\"".$city."\">
    		    <input type=\"submit\" value=\"Go\">
    		  </fieldset>
    		</form>
    	</center>";
		echo $anomaly_table;
		echo "Connected successfully-".$city;
		?>
	</body>
</html>

