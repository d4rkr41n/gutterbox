<!doctype html>
<head>
    <title>GutterBox</title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>

<body>
<table id="scan-table">

<?php
    $myPDO = new PDO('sqlite:/home/pi/scanned.db');
?>

<?php
    $targets = $myPDO->query("SELECT os,hostname,address,ports FROM targets");
    foreach($targets as $tar)
    {
        echo "<tr>";
        if($tar['os'] == "windows"){
            echo "<td class='windows'></td>";
        }else{
            echo "<td class='linux'></td>";
        }
        echo "<td>".$tar['hostname']."</td>";
        echo "<td>".$tar['address']."</td>";
        echo "<td>".$tar['ports']."</td>";
        echo "</tr>";
    }
?>

</table>
</body>
<html>