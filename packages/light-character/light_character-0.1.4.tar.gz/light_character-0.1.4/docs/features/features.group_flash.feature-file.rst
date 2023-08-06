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

:gherkin-feature-keyword:`Feature:` :gherkin-feature-content:`Group Flashing`
=============================================================================

    :gherkin-feature-description:`In a group flashing characteristic, a group of a specific number of flashes are repeated regularly.`

    :gherkin-feature-description:`As with a normal flashing characteristic, the light is on for a brief period, then off for a longer period.`

    :gherkin-feature-description:`There then follows a longer dark period before the pattern repeats again.`

:gherkin-scenario-keyword:`Scenario:` :gherkin-scenario-content:`Single group flash (e.g. Fl(3))`
-------------------------------------------------------------------------------------------------

| :gherkin-step-keyword:`When` I request an image with the characteristic Fl(3) R 10s
| :gherkin-step-keyword:`Then` the first frame is red for 0.5 seconds
| :gherkin-step-keyword:`And` the next frame is transparent for 1 second
| :gherkin-step-keyword:`And` the next frame is red for 0.5 seconds
| :gherkin-step-keyword:`And` the next frame is transparent for 1 second
| :gherkin-step-keyword:`And` the next frame is red for 0.5 seconds
| :gherkin-step-keyword:`And` the next frame is transparent for 6.5 seconds

:gherkin-scenario-keyword:`Scenario:` :gherkin-scenario-content:`Composite group flash (e.g. Fl(3+1))`
------------------------------------------------------------------------------------------------------

    :gherkin-scenario-description:`In a composite group flash, there are two grouped patterns separated by a longer period of darkness.`

    :gherkin-scenario-description:`The \"spare\" time between groups is evenly distributed.`

| :gherkin-step-keyword:`When` I request an image with the characteristic Fl(3+1) G 15s
| :gherkin-step-keyword:`Then` the first frame is green for 0.5 seconds
| :gherkin-step-keyword:`And` the next frame is transparent for 1 second
| :gherkin-step-keyword:`And` the next frame is green for 0.5 seconds
| :gherkin-step-keyword:`And` the next frame is transparent for 1 second
| :gherkin-step-keyword:`And` the next frame is green for 0.5 seconds
| :gherkin-step-keyword:`And` the next frame is transparent for 5.5 seconds
| :gherkin-step-keyword:`And` the next frame is green for 0.5 seconds
| :gherkin-step-keyword:`And` the next frame is transparent for 5.5 seconds

