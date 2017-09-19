-- This Source Code Form is subject to the terms of the Mozilla Public
-- License, v. 2.0. If a copy of the MPL was not distributed with this
-- file, You can obtain one at http://mozilla.org/MPL/2.0/.

--[[
# Runs Heka messages through the correspond parquet schema
--]]

local messages = {
    {
        Type = "telemetry.error",
        EnvVersion = "heka.telemetry_errors.1", -- schema specification for the test output
        Fields = {
            submissionDate = "20170622",
            docType = "main",
            appName = "Firefox",
            appVersion = "53.0.3",
            appUpdateChannel = "release",
            appBuildId = "20170518000419",
            DecodeErrorType = "json",
            DecodeError = "main schema version 4 validation error: xyz",
            geoCountry = "US",
            geoCity = "San Jose"
        }
    },
    {
        Type = "telemetry.duplicate",
        EnvVersion = "heka.telemetry_duplicates.1",
        Fields = {
            appBuildId = "20170518000419",
            appName = "Firefox",
            appUpdateChannel = "release",
            appVersion = "53.0.3",
            docType = "main",
            documentId = "e718b0ec-8d59-4f9d-90c4-25d1f2b53d98",
            duplicateDelta = {value = 1, value_type = 2},
            normalizedChannel = "release",
            geoCountry = "US",
            geoCity = "San Jose"
        }
    },
    {
        Type = "moz_ingest",
        EnvVersion = "heka.moz_ingest_uri_errors.1",
        Fields = {
            DecodeErrorType = "uri",
            DecodeError = "invalid uri",
            uri = "/foobar"
        }
    }
}


function process_message()
    for i,v in ipairs(messages) do
        inject_message(v)
    end
    return 0
end
