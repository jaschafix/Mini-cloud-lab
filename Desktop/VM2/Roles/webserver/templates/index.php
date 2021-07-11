<html>
<head>
	<title>{{host_name}}</title>
</head>
<body>
	<p>Welkom bij : {{host_name}}</p>

<?php 
$servername = "{{ hostvars[groups['database'][0]]['ansible_facts']['hostname'] }}";
$username = "root";
$password = "root";
$dbname = "testdb";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error){
	die("Connection failed: ". $conn->connect_error);
}

$sql = "SELECT * FROM test";
$result = $conn->query($sql);

if ($result->num_rows > 0){
	while ($row = $result->fetch_assoc()){
		echo "type server: ".$row['TypeServer']. " aantal: ". $row['AantalServers']. "<br>";
	}
}
?>
</body>
</html>