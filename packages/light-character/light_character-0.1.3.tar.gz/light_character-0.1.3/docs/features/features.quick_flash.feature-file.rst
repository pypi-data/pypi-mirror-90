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

:gherkin-feature-keyword:`Feature:` :gherkin-feature-content:`Quick Flash`
==========================================================================

    :gherkin-feature-description:`Quick flashes (Q) flash more than 50 times per minute`

:gherkin-scenario-outline-keyword:`Scenario Outline:` :gherkin-scenario-outline-content:`Quick Flash Period \<character\>`
--------------------------------------------------------------------------------------------------------------------------

    :gherkin-scenario-description:`The period of a flashing characteristic is the total time of the sequence.`

    :gherkin-scenario-description:`A quick flash is 0.25 seconds long, so the dark period is a quarter of a second`
    :gherkin-scenario-description:`shorter than the total period.`

| :gherkin-step-keyword:`When` I request an image with the characteristic **\<character\>**
| :gherkin-step-keyword:`Then` the first frame is **\<colour\>** for 0.25 seconds
| :gherkin-step-keyword:`And` the next frame is transparent for 0.75 seconds

:gherkin-examples-keyword:`Examples:`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table::
    :header: "character", "colour"
    :quote: “

    “Q W“, “white“
    “Q R“, “red“
    “Q G“, “green“
    “Q Y“, “yellow“

:gherkin-scenario-keyword:`Scenario:` :gherkin-scenario-content:`Illegal Quick Flash - continuous with period`
--------------------------------------------------------------------------------------------------------------

    :gherkin-scenario-description:`A simple Quick flash has no period`

| :gherkin-step-keyword:`When` I request an image with the characteristic Q. 1
| :gherkin-step-keyword:`Then` the request fails

