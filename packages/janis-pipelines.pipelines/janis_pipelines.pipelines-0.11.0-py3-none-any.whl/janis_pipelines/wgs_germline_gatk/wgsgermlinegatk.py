import operator
from typing import Optional, List

from janis_bioinformatics.data_types import FastqGzPair, Bam
from janis_bioinformatics.tools.babrahambioinformatics import FastQC_0_11_8
from janis_bioinformatics.tools.common import BwaAligner, MergeAndMarkBams_4_1_3
from janis_bioinformatics.tools.pmac import ParseFastqcAdaptors
from janis_core import String, Array, File
from janis_core.tool.test_classes import (
    TTestCase,
    TTestExpectedOutput,
    TTestPreprocessor,
)

from janis_pipelines.wgs_germline_gatk.wgsgermlinegatk_variantsonly import (
    WGSGermlineGATKVariantsOnly,
    INPUT_DOCS,
)


class WGSGermlineGATK(WGSGermlineGATKVariantsOnly):
    def id(self):
        return "WGSGermlineGATK"

    def friendly_name(self):
        return "WGS Germline (GATK)"

    def constructor(self):
        self.add_inputs()

        self.add_fastqc()
        self.add_align()

        self.add_bam_process()

        # mfranklin (2020-08-20): This is pretty cool, it allows us to reuse
        # these step definitions in different pipelines (without creating a whole subworkflow)

        self.add_bam_qc(bam_source=self.merge_and_mark.out)

        # Add variant callers
        self.add_gatk_variantcaller(bam_source=self.merge_and_mark.out)

    def add_inputs(self):
        # INPUTS
        self.input("sample_name", String, doc=INPUT_DOCS["sample_name"])
        self.input("fastqs", Array(FastqGzPair), doc=INPUT_DOCS["fastqs"])

        self.inputs_for_reference()
        self.inputs_for_intervals()
        self.inputs_for_configuration()

    def inputs_for_configuration(self):
        super().inputs_for_configuration()

        self.input("cutadapt_adapters", File, doc=INPUT_DOCS["cutadapt_adapters"])

    def add_fastqc(self):
        self.step("fastqc", FastQC_0_11_8(reads=self.fastqs), scatter="reads")

        self.output(
            "out_fastqc_reports",
            source=self.fastqc.out,
            output_folder="reports",
            doc="A zip file of the FastQC quality report.",
        )

    def add_align(self):
        self.step(
            "getfastqc_adapters",
            ParseFastqcAdaptors(
                fastqc_datafiles=self.fastqc.datafile,
                cutadapt_adaptors_lookup=self.cutadapt_adapters,
            ),
            scatter="fastqc_datafiles",
        )

        self.step(
            "align_and_sort",
            BwaAligner(
                fastq=self.fastqs,
                reference=self.reference,
                sample_name=self.sample_name,
                sortsam_tmpDir="./tmp",
                cutadapt_adapter=self.getfastqc_adapters,
                cutadapt_removeMiddle3Adapter=self.getfastqc_adapters,
            ),
            scatter=["fastq", "cutadapt_adapter", "cutadapt_removeMiddle3Adapter"],
        )

    def add_bam_process(self):
        self.step(
            "merge_and_mark",
            MergeAndMarkBams_4_1_3(
                bams=self.align_and_sort.out, sampleName=self.sample_name
            ),
        )

        self.output(
            "out_bam",
            source=self.merge_and_mark.out,
            output_folder="bams",
            doc="Aligned and indexed bam.",
            output_name=self.sample_name,
        )

    def tests(self) -> Optional[List[TTestCase]]:

        bioinf_base = "https://swift.rc.nectar.org.au/v1/AUTH_4df6e734a509497692be237549bbe9af/janis-test-data/bioinformatics"
        hg38 = f"{bioinf_base}/hg38"

        return [
            TTestCase(
                name="brca1",
                input={
                    "sample_name": "NA12878",
                    "reference": f"{hg38}/reference/Homo_sapiens_assembly38.fasta",
                    "fastqs": [
                        [
                            f"{bioinf_base}/BRCA1_R1.fastq.gz",
                            f"{bioinf_base}/BRCA1_R2.fastq.gz",
                        ]
                    ],
                    "gatk_intervals": [f"{hg38}/NA12878/BRCA1.bed"],
                    "known_indels": f"{hg38}/known_indels/Homo_sapiens_assembly38.known_indels.vcf.gz",
                    "mills_indels": f"{hg38}/mills_indels/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz",
                    "snps_1000gp": f"{hg38}/snps_1000GP/1000G_phase1.snps.high_confidence.hg38.vcf.gz",
                    "snps_dbsnp": f"{hg38}/snps_dbsnp/Homo_sapiens_assembly38.dbsnp138.vcf.gz",
                    "cutadapt_adapters": "https://raw.githubusercontent.com/csf-ngs/fastqc/master/Contaminants/contaminant_list.txt",
                },
                output=[
                    TTestExpectedOutput(
                        tag="out_variants_uncompressed",
                        preprocessor=TTestPreprocessor.LinesDiff,
                        file_diff_source=f"{hg38}/NA12878/brca1.germline.gatk.vcf",
                        operator=operator.eq,
                        expected_value=(1, 1),
                    ),
                    TTestExpectedOutput(
                        tag="out_bam",
                        preprocessor=TTestPreprocessor.Value,
                        operator=Bam.equal,
                        expected_value=f"{hg38}/NA12878/NA12878.bam",
                    ),
                ],
            )
        ]


if __name__ == "__main__":
    from toolbuilder.runtest.runner import run_test_case, EngineType

    tool = WGSGermlineGATK()
    # tool.translate("wdl")

    results = run_test_case(
        tool,
        test_case=tool.tests()[0].name,
        engine=EngineType.cromwell,
        # circumvent running tests by declaring outputs = {<outputs}>
        # output=outputs,
    )
    print(results)
