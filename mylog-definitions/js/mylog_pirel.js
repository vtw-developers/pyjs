"use strict";
const crypto = require("crypto");
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
  if (Number.isNaN(arg))
    return serializeString("nan");
  if (arg >= Number.MIN_SAFE_INTEGER && arg <= Number.MAX_SAFE_INTEGER) {
    return ["number", arg];
  }
  return serializeString(String(arg.toExponential(6)));
}

function serializeArray(arg) {
  const serializedVals = arg.map(val => serialize(val));
  const serializedValsStr = JSON.stringify(serializedVals);
  const hashed = crypto.createHash("sha256").update(serializedValsStr).digest("hex");
  return ["hash", hashed.length, hashed];
}

function serializeSet(arg) {
  const arrVals = Array.from(arg);
  let sortedVals;
  if (arrVals.length === 0) {
    sortedVals = arrVals;
  } else {
    const firstType = typeof arrVals[0];
    if (firstType === "string") {
      sortedVals = arrVals.slice().sort();
    } else if (firstType === "number") {
      sortedVals = arrVals.slice().sort((a, b) => a - b);
    } else {
      throw new Error("serializeSet only supports sets of strings or numbers");
    }
  }
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
  if (arg === null || typeof arg === "undefined")
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
  // myexactlog([...arguments]);
  // _default_console_log(...arguments);
};

// this function is inserted into body node types' `block`
function secret_fun_4071() {
  return 0;
}
