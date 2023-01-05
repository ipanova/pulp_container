Adding other OCI media types to Pulp Registry
=============================================

Helm, cosign, and OCI images mediatypes are built into the registry  by default.
For any other OCI media type that is not supported by default, you can add them to the ADDITIONAL_OCI_ARTIFACT_TYPES settings  using the following format::

 ADDITIONAL_OCI_ARTIFACT_TYPES = {
    "<oci config type 1>": [
        "<oci layer type A>",
        "<oci layer type B>",
    ],
    "<oci config type 2>": [
        "<oci layer type C>",
        "<oci layer type D>",
    ],
 }


For example, you can add Singularity (SIF) support by adding the following to your ADDITIONAL_OCI_ARTIFACT_TYPES setting::

 ADDITIONAL_OCI_ARTIFACT_TYPES = {
    "<oci config type 1>": [
        "<oci layer type A>",
        "<oci layer type B>",
    ],
    "<oci config type 2>": [
        "<oci layer type C>",
        "<oci layer type D>",
    ],
    "application/vnd.sylabs.sif.config.v1+json": [
        "application/vnd.sylabs.sif.layer.v1.sif"
    ],
 }

 .. note::

When adding OCI media types that are not configured by default, users will also need to manually add support for cosign and Helm if desired.
The OCI images mediatypes are supported by default, so users will not need to add that to enable support. 
