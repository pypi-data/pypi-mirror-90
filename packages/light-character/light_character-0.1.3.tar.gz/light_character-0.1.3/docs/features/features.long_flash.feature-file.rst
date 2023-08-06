.. role:: gherkin-step-keyword
.. role:: gherkin-step-content
.. role:: gherkin-feature-description
.. role:: gherkin-scenario-description
.. role:: gherkin-feature-keyword
.. role:: gherkin-feature-content
.. role:: gherkin-background-keyword
.. role:: gherkin-background-content
.. role:: gherkin-scenario-keyword
.. role:: gherkin-scenario-content
.. role:: gherkin-scenario-outline-keyword
.. role:: gherkin-scenario-outline-content
.. role:: gherkin-examples-keyword
.. role:: gherkin-examples-content
.. role:: gherkin-tag-keyword
.. role:: gherkin-tag-content

:gherkin-feature-keyword:`Feature:` :gherkin-feature-content:`Long Flash`
=========================================================================

    :gherkin-feature-description:`Long flashes (Lfl) are light for two seconds or more`

:gherkin-scenario-outline-keyword:`Scenario Outline:` :gherkin-scenario-outline-content:`Long Flash Period \<character\>`
-------------------------------------------------------------------------------------------------------------------------

    :gherkin-scenario-description:`The period of a flashing characteristic is the total time of the sequence.`

    :gherkin-scenario-description:`A long flash is 2 seconds long, so the dark period is two seconds shorter than`
    :gherkin-scenario-description:`the total period.`

| :gherkin-step-keyword:`When` I request an image with the characteristic **\<character\>**
| :gherkin-step-keyword:`Then` the first frame is **\<colour\>** for 2 seconds
| :gherkin-step-keyword:`And` the next frame is transparent for **\<dark_period\>** seconds

:gherkin-examples-keyword:`Examples:`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table::
    :header: "character", "colour", "dark_period"
    :quote: “

    “L.Fl W 5“, “white“, “3“
    “L.Fl R 10“, “red“, “8“
    “L.Fl G 7“, “green“, “5“
    “L.Fl Y 8“, “yellow“, “6“

