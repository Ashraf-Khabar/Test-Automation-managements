*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${BROWSER}    Chrome
${URL}        https://www.kayak.com/
${FROM_FIELD}    name=origin
${TO_FIELD}    name=destination
${SEARCH_BUTTON}    xpath=//button[contains(text(), 'Search')]
${RESULT_SECTION}    xpath=//div[contains(@class, 'resultsContainer')]

*** Test Cases ***
Test Recherche Vol Kayak
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    ${FROM_FIELD}    timeout=5s
    Input Text    ${FROM_FIELD}    Paris, France
    Input Text    ${TO_FIELD}    New York, USA
    Press Keys    ${TO_FIELD}    ENTER
    Wait Until Element Is Visible    ${RESULT_SECTION}    timeout=10s
    Element Should Be Visible    ${RESULT_SECTION}
    [Teardown]    Close Browser
