# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from setuptools import setup


setup(
    name="bio_embeddings-esm",
    version="0.2.1", # Patched for bio_embeddings
    description="Pre-trained evolutionary scale models for proteins, from Facebook AI Research.",
    author="Facebook AI Research",
    url="https://github.com/facebookresearch/esm",
    license="MIT",
    packages=["esm"],
    data_files=[("source_docs/esm", ["LICENSE", "README.md", "CODE_OF_CONDUCT.rst"])],
    zip_safe=True,
    install_requires=["torchvision"]
)
