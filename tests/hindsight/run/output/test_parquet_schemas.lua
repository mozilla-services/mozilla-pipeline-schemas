-- This Source Code Form is subject to the terms of the Mozilla Public
-- License, v. 2.0. If a copy of the MPL was not distributed with this
-- file, You can obtain one at http://mozilla.org/MPL/2.0/.

--[[
# Runs the sample JSON through the corresponding parquet output schema
--]]

require "cjson"
require "io"
require "lfs"
require "parquet"
require "string"
local parser = require "lpeg.parquet"

local function load_doctypes(namespace, path, schemas)
    for dn in lfs.dir(path) do -- iterate the schema diretories
        local fqdn = string.format("%s/%s", path, dn)
        local mode = lfs.attributes(fqdn, "mode")
        if mode == "directory" and not dn:match("^%.") then
            for fn in lfs.dir(fqdn) do -- iterate the schema files
                local schema, version = fn:match("(.+)%.(%d+)%.parquetmr.txt$")
                if schema then
                    local fqfn = string.format("%s/%s", fqdn, fn)
                    print("loading", fqfn)
                    local fh = assert(io.input(fqfn))
                    local ps = fh:read("*a")
                    fh:close()
                    schemas[string.format("%s.%s.%s", namespace, schema, version)] = parser.load_parquet_schema(ps)
                end
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


local schemas = load_schemas("../../schemas")
local metadata = {
    Timestamp = 1234,
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
    -- required pioneer metadata
    pioneerId = "11111111-1111-1111-1111-111111111111",
    studyName = "foobar",
    studyVersion = 1,
    }

function process_message()
    cjson.decode_null(true)
    local version = read_message("EnvVersion")
    if version then
        local schema = schemas[version]
        if not schema then return 0 end

        print("writing", version)
        local writer = parquet.writer("output/" .. version, schema)
        writer:dissect_message()
        writer:close()
    else
        local namespace = read_message("Type")
        local doctype = read_message("Fields[docType]")
        local version = read_message("Fields[sourceVersion]")
        local name = string.format("%s.%s.%s", namespace,  doctype,  version)
        local schema = schemas[name]
        if not schema then return 0 end

        print("writing", name)
        local writer = parquet.writer("output/" .. name, schema)
        local json = cjson.decode(read_message("Payload"))
        json.metadata = metadata
        writer:dissect_record(json)
        writer:close()
    end
    return 0
end


function timer_event()

end

