*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${BROWSER}    Chrome
${URL}        https://weather.com/
${SEARCH_FIELD}    xpath=//input[@type='text']
${SEARCH_RESULT}    xpath=//button[contains(@class, 'styles__item')]
${TEMPERATURE_DISPLAY}    xpath=//span[contains(@class, 'CurrentConditions')]

*** Test Cases ***
Test Recherche Météo
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    ${SEARCH_FIELD}    timeout=5s
    Input Text    ${SEARCH_FIELD}    Paris
    Press Keys    ${SEARCH_FIELD}    ENTER
    Wait Until Element Is Visible    ${TEMPERATURE_DISPLAY}    timeout=5s
    Element Should Be Visible    ${TEMPERATURE_DISPLAY}
    [Teardown]    Close Browser
