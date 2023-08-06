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

:gherkin-feature-keyword:`Feature:` :gherkin-feature-content:`Fixed Lights`
===========================================================================

    :gherkin-feature-description:`The Fixed pattern, F, is an always-on light in the given colour.`

:gherkin-scenario-keyword:`Scenario:` :gherkin-scenario-content:`Default white fixed light`
-------------------------------------------------------------------------------------------

| :gherkin-step-keyword:`When` I request an image with the characteristic F
| :gherkin-step-keyword:`Then` the image is a fixed white light

:gherkin-scenario-outline-keyword:`Scenario Outline:` :gherkin-scenario-outline-content:`Explicit fixed \<name\> light`
-----------------------------------------------------------------------------------------------------------------------

| :gherkin-step-keyword:`When` I request an image with the characteristic **\<character\>**
| :gherkin-step-keyword:`Then` the image is a fixed **\<name\>** light

:gherkin-examples-keyword:`Examples:`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table::
    :header: "character", "name"
    :quote: “

    “F W“, “white“
    “F R“, “red“
    “F G“, “green“
    “F Y“, “yellow“

