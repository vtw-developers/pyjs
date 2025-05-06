"use strict";
let _default_console_log = console.log;

function mylog_obj_to_comp(arg) {
  if (arg === true || arg === false) {
    return ["bool", arg];
  }
  if (typeof arg === "string") {
    return ["string", arg.length, arg];
  }
  if (typeof arg === "number") {
    return ["num", arg];
  }
  if (Array.isArray(arg)) {
    let rec_arg = arg.map((x) => mylog_obj_to_comp(is_exact, x))
    return ["list", arg.length, rec_arg];
  }
  if (arg === null) {
    return ["none"];
  }
  let str_result = String(arg);
  return ["Unknown", str_result.length, str_result];
}

function pirel_obj_serialize(key, value) {
  // sort the keys of an object before logging it to ensure the order of keys
  if (value && Object.prototype.toString.call(value) === "[object Object]") {
    return Object.keys(value)
      .sort() // Sort the keys alphabetically
      .reduce((sortedObj, sortedKey) => {
        sortedObj[sortedKey] = value[sortedKey];
        return sortedObj;
      }, {});
  }
  if (value && Object.prototype.toString.call(value) === "[object Set]") {
    return Array.from(value);
  }
  return value; // Return the value as-is for non-objects
}

function myexactlog(...args) {
  let prefix = "MYLOGEX:";
  let info_list = [prefix + JSON.stringify(args[0], pirel_obj_serialize)];
  for (let i = 1; i < args.length; i++) {
    info_list.push(mylog_obj_to_comp(args[i]));
  }
  _default_console_log(JSON.stringify(info_list));
}

console.log = function () {
  myexactlog([...arguments]);
  _default_console_log(...arguments);
};

// this function is inserted into body node types' `block`
function secret_fun_4071() {
  return 0;
}
