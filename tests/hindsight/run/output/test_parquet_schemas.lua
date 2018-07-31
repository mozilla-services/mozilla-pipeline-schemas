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

local metadata_group  = read_config("metadata_group")
local metadata_prefix = read_config("metadata_prefix")
local hive_compatible = read_config("hive_compatible")

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
                    local found_group
                    if ps:find("group%s+" .. metadata_group) then found_group = metadata_group end
                    local found_prefix
                    if ps:find(metadata_prefix, nil, true) then found_prefix = metadata_prefix end
                    schemas[string.format("%s.%s.%s", namespace, schema, version)] = {parser.load_parquet_schema(ps, hive_compatible, found_group, found_prefix)}
                end
            end
        elseif mode == "file" then
            local schema, version = dn:match("(.+)%.(%d+)%.parquetmr.txt$")
            if schema then
                print("loading", fqdn)
                local fh = assert(io.input(fqdn))
                local ps = fh:read("*a")
                fh:close()
                local found_group
                if ps:find("group%s+" .. metadata_group) then found_group = metadata_group end
                local found_prefix
                if ps:find(metadata_prefix, nil, true) then found_prefix = metadata_prefix end
                schemas[string.format("%s.%s.%s", namespace, schema, version)] = {parser.load_parquet_schema(ps, hive_compatible, found_group, found_prefix)}
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
function process_message()
    cjson.decode_null(true)
    local version = read_message("EnvVersion")
    if version then
        local schema = schemas[version]
        if not schema then return 0 end

        print("writing", version)
        local writer = parquet.writer("output/" .. version, schema[1])
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
        local writer = parquet.writer("output/" .. name, schema[1])
        local json = cjson.decode(read_message("Payload"))
        if schema[2] then schema[2](json) end
        writer:dissect_record(json)
        writer:close()
    end
    return 0
end


function timer_event()

end
