"use strict";
const SKIP_LOGGING = false;
const MYLOG_LIST = {MYLOG_LIST};
let _console_log = console.log;
let mylog_callcount = 0;

function _list_compare(ls1, ls2) {
  if (ls1.length !== ls2.length) {
    return false;
  }

  if (ls1.length > 0 && ls1[0] === "num" && ls2.length > 0 && ls2[0] === "num") {
    if (ls1[1] === ls2[1]) {
      return true;
    }

    try {
      if (Math.abs(ls1[1]) > 1e-6 && Math.abs(ls2[1]) > 1e-6) {
        if (Math.abs(ls1[1]) > 2 * Math.abs(ls2[1])) {
          return false;
        }
        if (2 * Math.abs(ls1[1]) < Math.abs(ls2[1])) {
          return false;
        }
        if (Math.abs(Math.abs(ls1[1] / ls2[1]) - 1) > 1e-6) {
          return false;
        }
        return true;
      }
      if (Math.abs(ls1[1]) <= 1e-6 && Math.abs(ls2[1]) <= 1e-6) {
        return true;
      }
      return false;
    } catch (e) {
      throw Error("MyLogError _list_compare num error: " + ls1 + " <==> " + ls2 + " " + e);
    }
  }

  if (ls1.length > 0 && ls1[0] === "string" && ls2.length > 0 && ls2[0] === "Unknown") {
    return ls1[2] === ls2[2];
  }

  let anyDiff = false;
  for (let i = 0; i < ls1.length; i++) {
    let ls1e = ls1[i],
      ls2e = ls2[i];
    if (Array.isArray(ls1e) && Array.isArray(ls2e)) {
      let elem_anydiff = !_list_compare(ls1e, ls2e);
      anyDiff = anyDiff || elem_anydiff;
    } else {
      anyDiff = anyDiff || ls1e !== ls2e;
    }
    if (anyDiff) {
      break;
    }
  }
  return !anyDiff;
}

function mylog_obj_to_comp(is_exact, arg) {
  let typearg = typeof arg;
  if (arg === true || arg === false) {
    return ["bool", arg];
  }
  if (typearg === "number") {
    return ["num", arg];
  }
  if (typearg === "string") {
    if (is_exact) {
      return ["string", arg.length, arg];
    }
    return ["string", arg.length, arg.length < 10 ? arg : arg.slice(0, 10)];
  }
  if (Array.isArray(arg)) {
    if (is_exact) {
      return ["list", arg.length, arg.map((x) => mylog_obj_to_comp(is_exact, x))];
    }
    return [
      "list",
      arg.length,
      arg.length > 0 ? mylog_obj_to_comp(is_exact, arg[0]) : "EMPTY",
      arg.length > 1 ? mylog_obj_to_comp(is_exact, arg[1]) : "EMPTY",
    ];
  }
  if (arg === null || arg === undefined) {
    return ["none"];
  }
  let str_result = String(arg);
  return ["Unknown", str_result.length, str_result];
}

function sortKeysReplacer(key, value) {
  // this function is used to sort the keys of an object
  // before logging it, to ensure that the order of keys  
  if (value && typeof value === "object" && !Array.isArray(value)) {
    return Object.keys(value)
      .sort() // Sort the keys alphabetically
      .reduce((sortedObj, sortedKey) => {
        sortedObj[sortedKey] = value[sortedKey];
        return sortedObj;
      }, {});
  }
  return value; // Return the value as-is for non-objects
}

function _mylog() {
  let is_exact = arguments[0];
  let prefix = is_exact ? "MYLOGEX:" : "MYLOGAP:";
  let info_list = [prefix + JSON.stringify(arguments[1], sortKeysReplacer)];
  if (SKIP_LOGGING === true && arguments[1] === -1) {
    return;
  }
  for (let i = 2; i < arguments.length; i++) {
    info_list.push(mylog_obj_to_comp(is_exact, arguments[i]));
  }
  _console_log(JSON.stringify(info_list));
  while (
    SKIP_LOGGING === true &&
    mylog_callcount < MYLOG_LIST.length &&
    MYLOG_LIST[mylog_callcount][0].endsWith(":-1")
  ) {
    mylog_callcount += 1;
  }
  if (mylog_callcount >= MYLOG_LIST.length) {
    throw Error(
      "MyLogError MYLOG_LENGTH_EXCEEDED COUNT:" + String(mylog_callcount) + " CALL_ID:" + String(arguments[0])
    );
  }
  if (_list_compare(info_list, MYLOG_LIST[mylog_callcount])) {
    mylog_callcount += 1;
    return;
  }
  throw Error(
    "MyLogError MISMATCH CALL_ID:" +
      String(arguments[1]) +
      " MISMATCH_IDX:" +
      String(mylog_callcount) +
      " OBSERVED:" +
      JSON.stringify(info_list) +
      " EXPECTED:" +
      JSON.stringify(MYLOG_LIST[mylog_callcount])
  );
}

function mylog() {
  _mylog(false, ...arguments);
}

function myexactlog() {
  _mylog(true, ...arguments);
}

console.log = function () {
  myexactlog(-1, [...arguments]);
  _console_log(...arguments);
};

// this function is inserted into body node types' `block`
function secret_fun_4071() {
  return 0;
}
