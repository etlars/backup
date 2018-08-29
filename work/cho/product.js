var os = require('os');

//simple but localhost
//var ips = require('child_process').execSync("ifconfig | grep inet | grep -v inet6 | awk '{gsub(/addr:/,\"\");print $2}'").toString().trim().split("\n");

function getIPAddresses() {

    var ipAddresses = [];

    var interfaces = require('os').networkInterfaces();
    for (var devName in interfaces) {
        var iface = interfaces[devName];
        for (var i = 0; i < iface.length; i++) {
            var alias = iface[i];
            if (alias.family === 'IPv4' && alias.address !== '127.0.0.1' && !alias.internal) {
                ipAddresses.push(alias.address);
            }
        }
    }

    //return ipAddresses;
    return ipAddresses[0];
}

var http = require('http');
var handleRequest = function(request, response) {
  response.writeHead(200);
//  response.end("Hello World! I'm server "+os.hostname() +", "+ips+" \n");
  response.end("Hello World! I'm Production server "+os.hostname() +", "+getIPAddresses()+" \n");

  //log
  console.log("["+
        Date(Date.now()).toLocaleString()+
        "] "+os.hostname());
}
var www = http.createServer(handleRequest);

www.listen(8080);
