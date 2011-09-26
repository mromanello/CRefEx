<?php
# using the library at http://keithdevens.com/software/xmlrpc
include("xmlrpc.php");
define("XMLRPC_DEBUG", 1);
$test=XMLRPC_request("www.mr56k.info:8001", "/rpc/crex", "json",array(XMLRPC_prepare("Hom. Il. 1.1 is a canonical citation")));
print($test[1]);
#XMLRPC_debug_print();
?>