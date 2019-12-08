var Log = function(msg, a) {
  mConsole = window.console;
  mConsole.log.apply(mConsole, arguments);
};

module.exports = Log;
