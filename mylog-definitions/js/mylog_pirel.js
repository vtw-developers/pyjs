"use strict";
let _default_console_log = console.log;

function serializeNull() {
  return ["null"];
}

function serializeBool(arg) {
  return ["bool", arg];
}

function serializeString(arg) {
  return ["string", arg.length, arg];
}

function serializeNum(arg) {
  if (arg === Infinity)
    return serializeString("inf");
  if (arg === -Infinity)
    return serializeString("-inf");
  return ["number", arg];
}

function serializeArray(arg) {
  const serializedVals = arg.map(val => serialize(val));
  return ["list", arg.length, serializedVals];
}

function serializeSet(arg) {
  const sortedVals = Array.from(arg).sort(); // Convert Set to Array and sort
  const serializedVals = sortedVals.map(val => serialize(val));
  return ["set", sortedVals.length, serializedVals];
}

function serializeObject(arg) {
  let serializedKeyValuePairs = [];
  const sortedKeys = Object.keys(arg).sort(); // Sort keys alphabetically
  for (const key of sortedKeys) {
      serializedKeyValuePairs.push(serialize([key, arg[key]]));
  }
  return ["dict", sortedKeys.length, serializedKeyValuePairs];
}

function serialize(arg) {
  if (arg === null)
    return serializeNull();
  if (arg === true || arg === false)
    return serializeBool(arg);
  if (typeof arg === "string")
    return serializeString(arg);
  if (typeof arg === "number")
    return serializeNum(arg);
  if (Array.isArray(arg))
    return serializeArray(arg);
  if (Object.prototype.toString.call(arg) === "[object Set]")
    return serializeSet(arg);
  if (Object.prototype.toString.call(arg) === "[object Object]")
    return serializeObject(arg);
  let str_result = String(arg);
  return ["unknown", str_result.length, str_result];
}

function myexactlog(...args) {
  let info_list = ["MYLOGEX:"];
  for (let i = 0; i < args.length; i++) {
    info_list.push(serialize(args[i]));
  }
  _default_console_log(JSON.stringify(info_list));
}

function mylog(...args) {
  myexactlog(...args);
}

console.log = function () {
  myexactlog([...arguments]);
  _default_console_log(...arguments);
};

// this function is inserted into body node types' `block`
function secret_fun_4071() {
  return 0;
}
