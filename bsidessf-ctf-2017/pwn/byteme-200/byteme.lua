#!/usr/bin/lua

key = "FLAG:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

-- Dump a string to hexpairs, stolen from the Internets
function hexdumpstr(str)
  return (
    string.gsub(str,"(.)",
      function (c)
        return string.format("%02X%s",string.byte(c), " ")
      end)
  )
end

if _VERSION ~= "Lua 5.2" then
  error("This code requires Lua 5.2!")
end

print("HELLO.")
print("GREET: Welcome to Direct-Inject Compute node software version 12.2.34.1a-build182398")
print("POWERED-BY: " .. _VERSION)
print("BYTECODE-VERSION: " .. hexdumpstr(string.sub(string.dump(loadstring('return')), 1, 12)) .. "...")
print("READY.")

code, e = load(io.read(140), nil, "b")
if not code then
  print("ERROR: " .. e)
else
  print("EXECUTING.")
  code()
end

print("BYE.")
