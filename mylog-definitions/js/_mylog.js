"use strict";
function mylog_obj_to_comp(arg) {
  let typearg = typeof arg;
  if (arg === true || arg === false) return ["bool", arg];
  else if (typearg === "number") return ["num", arg];
  else if (typearg === "string") return ["string", arg.length, arg.length < 10 ? arg : arg.slice(0,10)];
  else if (Array.isArray(arg)) return ["list", arg.length, arg.length > 0 ? mylog_obj_to_comp(arg[0]) : "EMPTY", arg.length > 1 ? mylog_obj_to_comp(arg[1]) : "EMPTY"];
  else if (arg === null || arg === undefined) return ["none"];
  else return ["Unknown"];
}
function mylog() {
  let info_list = ["MYLOG:" + arguments[0]];
  for (let i = 1; i < arguments.length; i++) {
    info_list.push(mylog_obj_to_comp(arguments[i]));
  }
  console.log("\\n" + JSON.stringify(info_list));
}
function myexactlog() {
  mylog(...arguments);
}