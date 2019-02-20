<!doctype html>
<head>
    <title>GutterBox</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
</head>

<body>

<h2>This might help</h2>
<p style="padding-top:0;"><a href="https://github.com/d4rkr41n"><i>- d4rkr41n</i></a></p>

<table id="scan-table">
<thead>
<tr class="table-header">
    <th>OS</td>
    <th>HOSTNAME</td>
    <th>ADDRESS</td>
    <th>PORTS</td>
</tr>
</thead>
<tbody>
<?php
    //echo class_exists("PDO");
    $myPDO = NULL;
    $myPDO = new PDO("sqlite:scanned.db");

    $targets = $myPDO->query("SELECT os,hostname,address,ports FROM targets");
    foreach($targets as $tar)
    {
        echo "\t<tr>\n";
        if(strtolower($tar['os']) == "windows"){
            echo "\t\t<td class='windows'><img src='media/windows.png'></td>\n";
        }else if(strtolower($tar['os']) == "linux"){
            echo "\t\t<td class='linux'><img src='media/linux.png'></td>\n";
        }else{
            echo "\t\t<td class='linux'><img src='media/unsure.png'></td>\n";
        }
        echo "\t\t<td>".$tar['hostname']."</td>\n";
        echo "\t\t<td>".$tar['address']."</td>\n";
        echo "\t\t<td>".$tar['ports']."</td>\n";
        echo "\t</tr>\n";
    }
?>

</tbody>
</table>
</body>
<html>
