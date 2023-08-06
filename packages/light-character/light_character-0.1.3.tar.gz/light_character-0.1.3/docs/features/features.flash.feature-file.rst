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

:gherkin-feature-keyword:`Feature:` :gherkin-feature-content:`Simple Flash`
===========================================================================

    :gherkin-feature-description:`A flash, Fl, is a brief period of light, followed by a longer period of darkness.`

:gherkin-scenario-outline-keyword:`Scenario Outline:` :gherkin-scenario-outline-content:`Flashing Period \<character\>`
-----------------------------------------------------------------------------------------------------------------------

    :gherkin-scenario-description:`The period of a flashing characteristic is the total time of the sequence.`

    :gherkin-scenario-description:`A flash is 1 second long, so the dark period is one second shorter than`
    :gherkin-scenario-description:`the total period.`

| :gherkin-step-keyword:`When` I request an image with the characteristic **\<character\>**
| :gherkin-step-keyword:`Then` the first frame is **\<colour\>** for 1 second
| :gherkin-step-keyword:`And` the next frame is transparent for **\<dark_period\>** seconds

:gherkin-examples-keyword:`Examples:`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table::
    :header: "character", "colour", "dark_period"
    :quote: “

    “Fl W 5“, “white“, “4“
    “Fl R 10“, “red“, “9“
    “Fl G 4“, “green“, “3“
    “Fl Y 8“, “yellow“, “7“

:gherkin-scenario-keyword:`Scenario:` :gherkin-scenario-content:`Illegal Flash`
-------------------------------------------------------------------------------

    :gherkin-scenario-description:`As a flash is one second, a cycle of 2 seconds or less is impossible.`

| :gherkin-step-keyword:`When` I request an image with the characteristic Fl 2
| :gherkin-step-keyword:`Then` the request fails

