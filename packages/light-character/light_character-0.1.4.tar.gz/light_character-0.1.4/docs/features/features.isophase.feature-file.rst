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

:gherkin-feature-keyword:`Feature:` :gherkin-feature-content:`Isophase Lights`
==============================================================================

    :gherkin-feature-description:`Isophase lights (Iso) are equally dark and light`

:gherkin-scenario-outline-keyword:`Scenario Outline:` :gherkin-scenario-outline-content:`Isophase Period \<character\>`
-----------------------------------------------------------------------------------------------------------------------

    :gherkin-scenario-description:`The cycle period of an isophase light is divided evenly between the light and dark`
    :gherkin-scenario-description:`periods`

| :gherkin-step-keyword:`When` I request an image with the characteristic **\<character\>**
| :gherkin-step-keyword:`Then` the first frame is **\<colour\>** for **\<period\>** seconds
| :gherkin-step-keyword:`And` the next frame is transparent for **\<period\>** seconds

:gherkin-examples-keyword:`Examples:`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table::
    :header: "character", "colour", "period"
    :quote: “

    “Iso W 6“, “white“, “3“
    “Iso R 10“, “red“, “5“
    “Iso G 7“, “green“, “3.5“
    “Iso Y 8“, “yellow“, “4“

