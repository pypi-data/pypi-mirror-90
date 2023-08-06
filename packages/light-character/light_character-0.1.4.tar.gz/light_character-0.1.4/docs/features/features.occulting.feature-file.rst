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

:gherkin-feature-keyword:`Feature:` :gherkin-feature-content:`Occulting`
========================================================================

    :gherkin-feature-description:`An occulting pattern (Oc) is basically the inverse of a flash. A short period`
    :gherkin-feature-description:`of darkness with a longer period of light.`

:gherkin-scenario-outline-keyword:`Scenario Outline:` :gherkin-scenario-outline-content:`Occulting characteristic \<character\>`
--------------------------------------------------------------------------------------------------------------------------------

    :gherkin-scenario-description:`The period of a characteristic is the total time of the sequence.`

    :gherkin-scenario-description:`A dark period is 1 second long, so the light period is one second shorter than`
    :gherkin-scenario-description:`the total period.`

| :gherkin-step-keyword:`When` I request an image with the characteristic **\<character\>**
| :gherkin-step-keyword:`Then` the first frame is transparent for 1 second
| :gherkin-step-keyword:`And` the next frame is **\<colour\>** for **\<light_period\>** second

:gherkin-examples-keyword:`Examples:`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table::
    :header: "character", "colour", "light_period"
    :quote: “

    “Oc W 5“, “white“, “4“
    “Oc R 10“, “red“, “9“
    “Oc G 4“, “green“, “3“
    “Oc Y 8“, “yellow“, “7“

