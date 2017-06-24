# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

cmake_minimum_required(VERSION 3.0)
project(mozilla-pipeline-schemas VERSION 0.0.1 LANGUAGES NONE)
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

file(GLOB_RECURSE SCHEMA_INCLUDES LIST_DIRECTORIES FALSE "${CMAKE_SOURCE_DIR}/templates/include/*")
foreach(ITEM IN ITEMS ${SCHEMA_INCLUDES})
  string(REGEX MATCHALL "/include/([^/]+)/([^/]+)\\.([0-9]+)\\..+(json|txt)$" PARTS ${ITEM})
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
  string(REGEX MATCH "^include/" MATCH ${ITEM})
  if(NOT MATCH)
    message("generating: schemas/" ${ITEM})
    # NOTE the artifacts are written back into the source repository (see the README)
    if(ITEM MATCHES "\\.json$") # pretty print
      configure_file("${CMAKE_SOURCE_DIR}/templates/${ITEM}" "${CMAKE_BINARY_DIR}/tmp.json" @ONLY)
      execute_process(COMMAND ${JQ_EXE} --sort-keys . RESULT_VARIABLE JQ_RV INPUT_FILE "${CMAKE_BINARY_DIR}/tmp.json" OUTPUT_FILE "${CMAKE_SOURCE_DIR}/schemas/${ITEM}")
      if(NOT JQ_RV EQUAL 0)
        message(FATAL_ERROR "invalid JSON ${ITEM}")
      endif()
    else()
      configure_file("${CMAKE_SOURCE_DIR}/templates/${ITEM}" "${CMAKE_SOURCE_DIR}/schemas/${ITEM}" @ONLY)
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
