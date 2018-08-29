var os = require('os');

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

    return ipAddresses[0];
}

var http = require('http');

http.createServer(onRequest_a).listen(8081);
http.createServer(onRequest_b).listen(8082);


function onRequest_a(request, response) {
  response.writeHead(200);
  response.end("App8081  server "+os.hostname() +", "+getIPAddresses()+" \n");
}

function onRequest_b(request, response) {
  response.writeHead(200);
  response.end("App8082  server "+os.hostname() +", "+getIPAddresses()+" \n");
}

