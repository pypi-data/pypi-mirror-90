from ipykernel.kernelapp import IPKernelApp
from .kernel import OracleKernel


IPKernelApp.launch_instance(kernel_class=OracleKernel)
