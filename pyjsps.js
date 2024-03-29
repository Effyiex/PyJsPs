
function PyPacket(label, args) {
  this.label = label;
  if(args != undefined) this.args = args;
  else this.args = [];
  this.parse = function() {
    var mapped = this.label;
    for(var i = 0; i < this.args.length; i++)
      mapped += PySocket.splitter + this.args[i];
    return mapped;
  }
  this.response = undefined;
  this.isPyPacket = true;
}

class PySocket {

  static PREFIX = "[PySocket]: ";

  static splitter = '\n';

  constructor(address, port, secured) {
    this.address = address;
    this.port = port;
    this.debug = true;
    if(secured != undefined)
    this.ssl = true;
  }

  static package = function(recv) {
    var mapped = recv.split(PySocket.splitter);
    if(mapped.length <= 0) return undefined;
    else {
      var label = mapped[0];
      var args = [];
      for(var i = 1; i < mapped.length; i++)
        args[i - 1] = mapped[i];
      return new PyPacket(label, args);
    }
  }

  log(info) {
    if(this.debug)
    console.log(PySocket.PREFIX + info);
  }

  send(packet, recv) {
    if(!packet.isPyPacket) {
      this.log("Script tried to send wrong Packet-Type: " + (typeof packet));
      return undefined;
    }
    var server = this.address + ':' + this.port;
    var socket = new WebSocket((this.ssl ? "wss://" : "ws://") + server);
    this.log("Sending to \"" + server  + "\": " + packet.label);
    socket.onopen = function(event) { socket.send(packet.parse()); }
    if(recv) socket.onmessage = function(event) { recv(PySocket.package(event.data)); }
  }

}
