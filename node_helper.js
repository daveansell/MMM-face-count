var NodeHelper = require("node_helper");
var lastDetect = 0;
var currentPage =-1;
var thethis;
module.exports = NodeHelper.create({
  socketNotificationReceived: function(notification, payload) {
    console.log("MMM-face_count");
    let DEBUG = payload["debug"];
    let blankTime = payload["blankTime"];
    var thethis = this;
    var lights = require("child_process").spawn("sudo", [
                       "python3",
                        __dirname + "/lights.py",

    ]);
    lights.stdin.setEncoding('utf-8');
    lights.stdin.write("0\n");

    // creating demon spawn
    var child = require("child_process").spawn(__dirname + "/facetracker_haar.py"
	    ,[],{ stdio: ['pipe', null, null, null, 'pipe'] });
    console.log("loaded child");
    // using arrow function to keep "this" reference of outer scope
    child.stdout.on("data", (data) => {
	  data=data.toString();
	  console.log("data=",data);
	  lastDetect = Date.now();
	  this.sendSocketNotification("PAGE_ACTIVATE", 1);
	  lights.stdin.write("1\n");
    });
    setInterval(function(){
      	if(Date.now()-lastDetect > blankTime){
	  thethis.sendSocketNotification("PAGE_DEFAULT", 0);
	  lights.stdin.write("0\n");
      }
    }, 500);

    child.stdout.on("exit", function(exitCode) {
      lights.stdin.write("q\n");
      console.log(exitCode);
    });
  },
});
