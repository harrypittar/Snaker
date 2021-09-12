<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<html>
<head><title>Snaker High Scores</title>
<style>
th { text-align: left; }

table, th, td {
  border: 2px solid grey;
  border-collapse: collapse;
}

th, td {
  padding: 0.2em;
}
</style>
</head>

<body>
<h1>Snaker</h1>

<p>High scores:</p>

<table border="1">
<tr><th>Username</th><th>High Score</th></tr>

<?php

$db_host   = '192.168.2.12';
$db_name   = 'snaker';
$db_user   = 'webuser';
$db_passwd = 'insecure_db_pw';

$pdo_dsn = "mysql:host=$db_host;dbname=$db_name";

$pdo = new PDO($pdo_dsn, $db_user, $db_passwd);

$q = $pdo->query("SELECT * FROM highscores");

while($row = $q->fetch()){
  echo "<tr><td>".$row["username"]."</td><td>".$row["score"]."</td></tr>\n";
}

?>
</table>
</body>
</html>
