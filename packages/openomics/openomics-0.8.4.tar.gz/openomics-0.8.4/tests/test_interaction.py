from openomics.database import MiRTarBase, STRING, LncRNA2Target
from .test_multiomics import *


@pytest.fixture
def generate_LncRNA2Target():
    return LncRNA2Target(version="low_throughput")

def test_import_LncRNA2Target(generate_LncRNA2Target):
    assert generate_LncRNA2Target.data_path is not None


@pytest.fixture
def generate_MiRTarBase():
    return MiRTarBase(path="/data/datasets/Bioinformatics_ExternalData/miRTarBase/", strip_mirna_name=True,
                      filters={"Species (Target Gene)": "Homo sapiens"})


def test_import_MiRTarBase(generate_MiRTarBase):
    assert generate_MiRTarBase.data_path is not None


@pytest.fixture
def generate_STRING():
    return STRING(edge_attr=["score"])


def test_import_STRING(generate_STRING):
    assert generate_STRING.data_path is not None


def test_annotate_STRING(generate_TCGA_LUAD, generate_STRING):
    generate_TCGA_LUAD.Protein.annotate_sequences(generate_STRING, index="protein_name")
    assert not generate_TCGA_LUAD.Protein.annotations["sequence"].empty
