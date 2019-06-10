# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

cmake_minimum_required(VERSION 3.0)
project(mozilla-pipeline-schemas VERSION 0.0.9 LANGUAGES NONE)
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Mozilla data ingestion and data lake schemas")

set(CPACK_PACKAGE_VERSION_MAJOR  ${PROJECT_VERSION_MAJOR})
set(CPACK_PACKAGE_VERSION_MINOR  ${PROJECT_VERSION_MINOR})
set(CPACK_PACKAGE_VERSION_PATCH  ${PROJECT_VERSION_PATCH})
set(CPACK_PACKAGE_VENDOR         "Mozilla Services")
set(CPACK_PACKAGE_CONTACT        "Mike Trinkala <trink@mozilla.com>")
set(CPACK_RESOURCE_FILE_LICENSE  "${CMAKE_SOURCE_DIR}/LICENSE.txt")
set(CPACK_RPM_PACKAGE_LICENSE    "MPLv2.0")

find_program(JQ_EXE jq)
if(NOT JQ_EXE)
  message(FATAL_ERROR "jq is required for output formatting")
endif()

find_program(PARQUETFMT_EXE parquetfmt)
if(NOT PARQUETFMT_EXE)
  if(WIN32)
    file(DOWNLOAD https://github.com/trink/parquetfmt/releases/download/v0.1.0/parquetfmt-win64.zip ./parquetfmt-win64.zip EXPECTED_MD5 d8ceb24e2d42ecb7fe286ede61e36e01)
    execute_process(COMMAND ${CMAKE_COMMAND} -E tar x parquetfmt-win64.zip)
  elseif(APPLE)
    file(DOWNLOAD https://github.com/trink/parquetfmt/releases/download/v0.1.0/parquetfmt-osx.zip ./parquetfmt-osx.zip EXPECTED_MD5 750d88084d3df4fc4f747de7d12a5e27)
    execute_process(COMMAND ${CMAKE_COMMAND} -E tar x parquetfmt-osx.zip)
  else()
    file(DOWNLOAD https://github.com/trink/parquetfmt/releases/download/v0.1.0/parquetfmt-linux.tgz ./parquetfmt-linux.tgz EXPECTED_MD5 a4ecfb3ba777ca698501f5fbe273bb48)
    execute_process(COMMAND ${CMAKE_COMMAND} -E tar x parquetfmt-linux.tgz)
  endif()
  find_program(PARQUETFMT_EXE parquetfmt HINTS ${CMAKE_CURRENT_BINARY_DIR})
endif()

file(GLOB_RECURSE SCHEMA_INCLUDES LIST_DIRECTORIES FALSE "${CMAKE_SOURCE_DIR}/templates/include/*")
foreach(ITEM IN ITEMS ${SCHEMA_INCLUDES})
  string(REGEX MATCHALL "/include/([^/]+)/([^/]+)\\.([1-9][0-9]*)\\..+(json|txt)$" PARTS ${ITEM})
  if( PARTS )
    string(TOUPPER "${CMAKE_MATCH_1}_${CMAKE_MATCH_2}_${CMAKE_MATCH_3}_${CMAKE_MATCH_4}" VARNAME)
    set(INCLUDE_TEMPLATES ${INCLUDE_TEMPLATES} ${VARNAME})
    file(READ ${ITEM} ${VARNAME})
  endif()
endforeach()

foreach(ITEM IN ITEMS ${INCLUDE_TEMPLATES})  # expand the variables in the include templates
  while("${${ITEM}}" MATCHES "@.+@")
    string(CONFIGURE "${${ITEM}}" ${ITEM} @ONLY)
  endwhile()
endforeach()

file(GLOB_RECURSE SCHEMAS LIST_DIRECTORIES FALSE RELATIVE "${CMAKE_SOURCE_DIR}/templates" "${CMAKE_SOURCE_DIR}/templates/*")
foreach(ITEM IN ITEMS ${SCHEMAS})
  if(NOT ITEM MATCHES "^(include/|.*/\\.[^/])" )
    string(REGEX MATCH "/([-a-zA-Z0-9_]+\\.[1-9][0-9]*\\.schema\\.json|[-a-zA-Z0-9_]+\\.[1-9][0-9]*\\.parquetmr\\.txt|README.*)$" MATCH ${ITEM})
    if(NOT MATCH)
      message(FATAL_ERROR "schema name contains invalid characters: " ${ITEM})
    endif()
    message("generating: schemas/" ${ITEM})
    # NOTE the artifacts are written back into the source repository (see the README)
    set(IN_FILE "${CMAKE_SOURCE_DIR}/templates/${ITEM}")
    set(OUT_FILE "${CMAKE_SOURCE_DIR}/schemas/${ITEM}")
    if(ITEM MATCHES "\\.json$") # pretty print
      set(TMP_FILE "${OUT_FILE}.tmp")
      configure_file(${IN_FILE} ${TMP_FILE} @ONLY)
      execute_process(COMMAND ${JQ_EXE} --sort-keys . RESULT_VARIABLE JQ_RV INPUT_FILE ${TMP_FILE} OUTPUT_FILE ${OUT_FILE})
      if(NOT JQ_RV EQUAL 0)
        message(FATAL_ERROR "jq output error ${JQ_RV} ${ITEM}")
      endif()
      file(REMOVE ${TMP_FILE}) # the tmp file is intentionally not removed on failure so it can be examined
    elseif(ITEM MATCHES "\\.parquetmr\\.txt$")
      set(TMP_FILE "${OUT_FILE}.tmp")
      configure_file(${IN_FILE} ${TMP_FILE} @ONLY)
      execute_process(COMMAND ${PARQUETFMT_EXE} - RESULT_VARIABLE PFMT_RV INPUT_FILE ${TMP_FILE} OUTPUT_FILE ${OUT_FILE})
      if(NOT PFMT_RV EQUAL 0)
        message(FATAL_ERROR "parquetfmt output error ${PFMT_RV} ${ITEM}")
      endif()
      file(REMOVE ${TMP_FILE}) # the tmp file is intentionally not removed on failure so it can be examined
    elseif(ITEM MATCHES "/README\\.")
      # ignore README files
    else()
      configure_file(${IN_FILE} ${OUT_FILE} @ONLY)
    endif()
  endif()
endforeach()

include(CTest)
add_custom_target(${PROJECT_NAME}-copy-tests ALL COMMAND ${CMAKE_COMMAND} -E copy_directory
${CMAKE_CURRENT_SOURCE_DIR}/tests
${CMAKE_CURRENT_BINARY_DIR})

add_test(NAME ${PROJECT_NAME}-hindsight COMMAND run.sh CONFIGURATIONS hindsight
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/hindsight)

include(GNUInstallDirs)
install(DIRECTORY "${CMAKE_SOURCE_DIR}/schemas/" DESTINATION "${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME}/")
include(CPack)
