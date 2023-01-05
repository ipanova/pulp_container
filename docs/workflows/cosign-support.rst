.. _cosign-support:

Install cosign
==============

Check for the file in https://github.com/sigstore/cosign/releases

Binary::

 wget "https://github.com/sigstore/cosign/releases/download/v1.6.0/cosign-linux-amd64"
 mv cosign-linux-amd64 /usr/local/bin/cosign
 chmod +x /usr/local/bin/cosign

Rpm::

 wget "https://github.com/sigstore/cosign/releases/download/v1.6.0/cosign-1.6.0.x86_64.rpm"
 rpm -ivh cosign-1.6.0.x86_64.rpm

Mirror
======

Being an OCI compliant registry Pulp Container registry can natively mirror cosign signatures
wich are stored as an OCI image::

 {
    "schemaVersion": 2,
    "mediaType": "application/vnd.oci.image.manifest.v1+json",
    "config": {
        "mediaType": "application/vnd.oci.image.config.v1+json",
        "digest": "sha256:f35028aa1563f37ccbaa0b32c57777ffbd8e9e3d81d739fec0022995e58a375a",
        "size": 153
    },
    "layers": [
        {
            "mediaType": "application/vnd.dev.cosign.simplesigning.v1+json",
            "digest": "sha256:d3370bd32b32aba43de2b45bb4a2de2fb5c95fd2edbe738acbc3bc595b80c456",
            "size": 305,
            "annotations": {
                "dev.cosignproject.cosign/signature": "MEUCIBWDnTKhbf5x3mSuEHWkv3ixloIFXeDpfXipF9szqrd5AiEA+UU5J84gQ9JnmT6QZAXiPXqSoDVW0CXQYssGh63e9Ro="
            }
        }
    ]
 }


During the syncronization task, Pulp will automatically mirror cosign signatures or atomic
signatures (accessible via signatures extentions API).


Sign
====

Pulp Container registry can host cosign signature which can be pushed via cosign or podman clients:

Cosign::


  # This command creates an ECDSA-P256 key pair (a private and a public key). 
  cosign generate-key-pair
  cosign sign --key cosign.key pulp-registry/ipanova/cosign-test:latest

or via Podman::

  podman push pulp-registry/ipanova/cosign-test:latest --sign-by-sigstore-private-key cosign.key

.. warning::
   To use this with images hosted on image registries, the relevant registry or repository must have
   the use-sigstore-attachments option enabled in containers-registries.d(5). This specifies whether
   sigstore image attachments (signatures, attestations and the like) are going to be read/written
   along with the image. If disabled, the images are treated as if no attachments exist; attempts to
   write attachments fail.

As a result of this operation ``ipanova/cosign-test:latest`` image is signed and its
cosign signature is stored in the registry as an OCI image. Cosign uses a fixed naming convention
to decide the name for a separate image, at which we can store the signature. The tag name resolved
to a fixed digest of the image/or manifest list which is being signed in a form of ``sha256-12345.sig``

The payload of the signature will be store as an image layer::

  {
    "critical": {
        "identity": {
            "docker-reference": "pulp-registry/ipanova/cosigned:latest"
        },
        "image": {
            "docker-manifest-digest": "sha256:81cd171c4eda75046c31d6ed26f1241bbfa9326640613430be780ea931b02c24"
        },
        "type": "cosign container image signature"
    },
    "optional": {
        "creator": "containers/image 5.23.1",
        "timestamp": 1673006074
    }
  }


.. note:
    Besides cosign signature Pulp Container Registry can mirror and host SBOMs and attestations.


The verify
==========

Signature verification can be done via cosign or podman clients::

  cosign verify --key cosign.pub pulp-registry/ipanova/cosign-test:latest

When using podman client the policy.json file should be properly configured per specs.
A new requirement type ``sigstoreSigned`` has been introduced:

https://github.com/containers/image/blob/main/docs/containers-policy.json.5.md#sigstoresigned

.. warning::
   To use this with images hosted on image registries, the relevant registry or repository must have
   the use-sigstore-attachments option enabled in containers-registries.d(5). This specifies whether
   sigstore image attachments (signatures, attestations and the like) are going to be read/written
   along with the image. If disabled, the images are treated as if no attachments exist; attempts to
   write attachments fail.
