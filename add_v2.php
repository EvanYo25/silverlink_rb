<?php 
        echo "<br>",var_dump($_POST),"<br>"; 



        $db = pg_connect('host=silverrb.lu.im.ntu.edu.tw port=5432 dbname=silver user=silver_root password=23174224silver');

        $time = pg_escape_string($_POST['inputtime']);
        $memo = pg_escape_string($_POST['memo']);
        $xvalue = pg_escape_string($_POST['xvalue']);
        $yvalue = pg_escape_string($_POST['yvalue']);
        $zvalue = pg_escape_string($_POST['zvalue']);

        $query = "INSERT INTO data1(timeinsert,xvalue,yvalue,zvalue,comment) VALUES('" . $time . "','" . $xvalue . "','" . $yvalue . "','" . $zvalue . "','" . $memo . "')";
        $result = pg_query($query); 
        if (!$result) { 
            $errormessage = pg_last_error(); 
            echo "Error with query: " . $errormessage;
            exit(); 
        } 
        printf ("values were inserted into the database ");
        pg_close(); 
?>
