Dataset **Apple Dataset Benchmark from Orchard Environment** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMjIzMV9BcHBsZSBEYXRhc2V0IEJlbmNobWFyayBmcm9tIE9yY2hhcmQgRW52aXJvbm1lbnQvYXBwbGUtZGF0YXNldC1iZW5jaG1hcmstZnJvbS1vcmNoYXJkLWVudmlyb25tZW50LURhdGFzZXROaW5qYS50YXIiLCAic2lnIjogImVKaDJvaDhTRi9aRmdRa0RWbW1ObmZUY0VkOGx2K3djeHNCQ1NPU0Zvalk9In0=?response-content-disposition=attachment%3B%20filename%3D%22apple-dataset-benchmark-from-orchard-environment-DatasetNinja.tar%22)

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
