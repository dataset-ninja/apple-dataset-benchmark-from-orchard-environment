Dataset **Apple Dataset Benchmark from Orchard Environment** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzIyMzFfQXBwbGUgRGF0YXNldCBCZW5jaG1hcmsgZnJvbSBPcmNoYXJkIEVudmlyb25tZW50L2FwcGxlLWRhdGFzZXQtYmVuY2htYXJrLWZyb20tb3JjaGFyZC1lbnZpcm9ubWVudC1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICJ1N1IxUlQ1bmtFNmhCQk1uRnpLVTRnT1lidSttMFR1SXBFWWR5dkpXUHpNPSJ9)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Apple Dataset Benchmark from Orchard Environment', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be downloaded here:

- [ArtificialLight.zip](https://rex.libraries.wsu.edu/view/fileRedirect?instCode=01ALLIANCE_WSU&filePid=13356462160001842&download=true)
- [CropLoadEstimation.zip](https://rex.libraries.wsu.edu/view/fileRedirect?instCode=01ALLIANCE_WSU&filePid=13356462140001842&download=true)
- [HarvestingRobot2016.zip](https://rex.libraries.wsu.edu/view/fileRedirect?instCode=01ALLIANCE_WSU&filePid=13356462080001842&download=true)
- [HarvestingRobot2017.zip](https://rex.libraries.wsu.edu/view/fileRedirect?instCode=01ALLIANCE_WSU&filePid=13356462040001842&download=true)
