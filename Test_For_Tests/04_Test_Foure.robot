*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${BROWSER}    Chrome
${URL}        https://www.unitconverters.net/
${CATEGORY_LINK}    xpath=//a[text()='Length']
${INPUT_FIELD}    id=fromVal
${OUTPUT_FIELD}    id=toVal
${UNIT_SELECTOR}    id=calFrom
${TARGET_UNIT}    id=calTo

*** Test Cases ***
Test Conversion Unité
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    ${CATEGORY_LINK}    timeout=5s
    Click Element    ${CATEGORY_LINK}
    Wait Until Element Is Visible    ${INPUT_FIELD}    timeout=5s
    Input Text    ${INPUT_FIELD}    10
    Select From List By Label    ${UNIT_SELECTOR}    Meters
    Select From List By Label    ${TARGET_UNIT}    Kilometers
    Sleep    2s
    Element Should Contain    ${OUTPUT_FIELD}    0.01
    [Teardown]    Close Browser
