-- This Source Code Form is subject to the terms of the Mozilla Public
-- License, v. 2.0. If a copy of the MPL was not distributed with this
-- file, You can obtain one at http://mozilla.org/MPL/2.0/.

--[[
# Runs the sample JSON through the generated schemas
--]]

require "io"
require "lfs"
require "rjson"
require "string"

local function read_file(fn)
    print("loading", fn)
    local fh = assert(io.input(fn))
    local s = fh:read("*a")
    fh:close()
    return s
end


local function load_doctypes(namespace, path, schemas)
    local doc = rjson.parse("{}")
    local js = read_file("jsonschema.4.json")
    local jsonschema = rjson.parse_schema(js)

    for dn in lfs.dir(path) do -- iterate the schema directories
        local fqdn = string.format("%s/%s", path, dn)
        local mode = lfs.attributes(fqdn, "mode")
        if mode == "directory" and not dn:match("^%.") then
            for fn in lfs.dir(fqdn) do -- iterate the schema files
                local schema, version = fn:match("(.+)%.(%d+)%.schema.json$")
                if schema then
                    local fqfn = string.format("%s/%s", fqdn, fn)
                    local js = read_file(fqfn)
                    doc:parse(js, true)
                    local ok, err = doc:validate(jsonschema)
                    if not ok then error(string.format("schema: %s error: %s", fqfn, err)) end
                    schemas[string.format("%s.%s.%s", namespace, schema, version)] = rjson.parse_schema(js)
                end
            end
        elseif mode == "file" then -- accept the new flattened generic ingestion directories
            local schema, version = dn:match("(.+)%.(%d+)%.schema.json$")
            if schema then
                js = read_file(fqdn)
                doc:parse(js, true)
                local ok, err = doc:validate(jsonschema)
                if not ok then error(string.format("schema: %s error: %s", fqfn, err)) end
                schemas[string.format("%s.%s.%s", namespace, schema, version)] = rjson.parse_schema(js)
            end
        end
    end
end


local function load_schemas(path)
    local schemas = {}
    for dn in lfs.dir(path) do -- iterate the namespace directories
        local fqdn = string.format("%s/%s", path, dn)
        local mode = lfs.attributes(fqdn, "mode")
        if mode == "directory" and not dn:match("^%.") then
            load_doctypes(dn, fqdn, schemas)
        end
    end
    return schemas
end


function process_message()
    local schemas = load_schemas("../../schemas")
    local doc = rjson.parse("{}")
    local msg = {
        Type = nil,
        Payload = nil,
        Fields = {
            docType = nil,
            sourceVersion = 0,
            creationTimestamp = 5678,
            submissionDate = "20170621",
            Date = "Wed, 21 Jun 2017 19:59:56 GMT",
            normalizedChannel = "release",
            geoCountry = "US",
            geoCity = "San Jose",
            documentId = "5F8D1153-CD83-40BB-B535-00708B027548",
            appBuildId = "20170711165157",
            appName = "Firefox",
            appUpdateChannel = "release",
            Host = "incoming.telemetry.mozilla.org",
            -- required pioneer metadata
            pioneerId = "11111111-1111-1111-1111-111111111111",
            studyName = "foobar",
            studyVersion = 1,
            -- required mobile-event metadata
            appVersion = "1.0.0",
            sampleId = 1
        }
    }

    local path = "../../validation"
    for namespace in lfs.dir(path) do
        local fqdn = string.format("%s/%s", path, namespace)
        local mode = lfs.attributes(fqdn, "mode")
        if mode == "directory" and not namespace:match("^%.") then
            for fn in lfs.dir(fqdn) do
                local schema, version, test, outcome = fn:match("(.+)%.(%d+)%.([%w_-]+)%.(pass)%.json$")
                if not schema then
                    schema, version, test, outcome = fn:match("(.+)%.(%d+)%.([%w_-]+)%.(fail)%.json$")
                end
                if not schema and fn:match("%.json$") then
                    error(string.format("found '%s' filename should be <schema>.<version>.<test_name>.<pass|fail>.json", fn))
                end
                if schema then
                    local fqfn = string.format("%s/%s", fqdn, fn)
                    local json = read_file(fqfn)
                    doc:parse(json, true)

                    local ok, err = doc:validate(schemas[string.format("%s.%s.%s", namespace, schema, version)])
                    if outcome == "pass" then
                        if not ok then error(err) end
                        msg.Type = namespace
                        msg.Fields.docType = schema
                        msg.Fields.sourceVersion = tonumber(version)
                        msg.Payload = json
                        inject_message(msg)
                    else -- "fail"
                        if ok then error(string.format("Validation should not have passed: %s", fn)) end
                    end
                end
            end
        end
    end
    return 0
end
