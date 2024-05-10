from Bio import SeqIO
import os
import re
import sys
import argparse
import pandas as pd
from multiprocessing import Pool, cpu_count

class ChromosomeNameExtractor:
    """
    用于从FASTA文件中提取染色体名称的类。
    
    参数:
    fasta_file (str): 包含染色体序列的FASTA文件路径。
    
    方法:
    list_chromosome_names: 提取并返回FASTA文件中的所有染色体名称的集合。
    """
    def __init__(self, fasta_file):
        self.fasta_file = fasta_file

    def list_chromosome_names(self):
        """
        提取并返回FASTA文件中的所有染色体名称的集合。
        
        返回:
        set: 染色体名称的集合。
        """
        if not self.fasta_file:
            raise ValueError("FASTA 文件路径未设置")
        chrom_names = set()
        with open(self.fasta_file, "r") as file:
            for record in SeqIO.parse(file, "fasta"):
                chrom_names.add(record.id)
        return chrom_names

class BEDChromosomeModifier:
    """
    用于修改BED文件中染色体名称的类。
    
    参数:
    filename (str): 输入的BED文件路径。
    valid_chromosomes (set): 有效的染色体名称集合。
    
    方法:
    modify_chromosomes: 将BED文件中的染色体名称修改为统一格式。
    save_to_file: 将修改后的数据保存到新的BED文件中。
    """
    def __init__(self, filename, valid_chromosomes):
        """
        初始化BEDChromosomeModifier实例。
        
        参数:
        filename (str): 输入的BED文件路径。
        valid_chromosomes (set): 有效的染色体名称集合。
        """
        self.filename = filename
        self.valid_chromosomes = valid_chromosomes
        self.data = pd.read_csv(filename, sep="\t", header=None)
        self.data.columns = ["chromosome", "start", "end"] + list(range(3, len(self.data.columns)))

    def modify_chromosomes(self,valid_chromosomes):
        """
        修改BED文件中的染色体名称,统一格式。
        """
 # 定义一个内部函数,用于修改染色体名称
        def modify(chrom):
            # 对染色体名称应用不同的转换规则
            if chrom.isdigit():
                modified = "chr" + chrom
            elif chrom == "MT":
                modified = "chrM"
            elif chrom == "X" or chrom == "Y":
                modified = "chr" + chrom
            else:
                modified_t1 =  "_" + chrom.replace(".", "v")
                regular_expression = ".*("+ modified_t1 + ").*"
                suffix_pattern = re.compile(regular_expression)
                match = suffix_pattern.match(modified_t1)
                if match:
                    # 在有效染色体列表中查找匹配的染色体名称
                    for valid_chrom in valid_chromosomes:
                        if match.group(1) in valid_chrom:
                            modified = valid_chrom
            return modified
        # 修改所有的染色体名称
        self.data["chromosome"] = self.data["chromosome"].apply(modify)
    def save_to_file(self, output_filename):
        """
        将修改后的BED数据保存到文件。
        
        参数:
        output_filename (str): 输出文件的路径。
        """
        self.data.to_csv(output_filename, sep="\t", header=False, index=False)

def process_file(bed_path, fasta_chromosomes, folderOfOutput):
    """
    处理单个BED文件,修改染色体名称,并保存到输出文件夹。
    
    参数:
    bed_path (str): 输入的BED文件路径。
    fasta_chromosomes (set): 从FASTA文件提取的有效染色体名称集合。
    folderOfOutput (str): 输出文件夹路径。
    """
    modifier = BEDChromosomeModifier(bed_path, fasta_chromosomes)
    modifier.modify_chromosomes(fasta_chromosomes)
    output_path = os.path.join(folderOfOutput, os.path.splitext(os.path.basename(bed_path))[0] + ".modified.bed")
    modifier.save_to_file(output_path)

def main(pathOfFasta, folderOfBED, folderOfOutput):
    """
    主函数,用于读取FASTA文件中的染色体名称,处理所有BED文件,并将修改后的结果保存到输出文件夹。

    参数:
    pathOfFasta (str): FASTA文件路径。
    folderOfBED (str): BED文件所在的文件夹路径。
    folderOfOutput (str): 输出文件夹路径。
    """
    fasta_chromosomes = ChromosomeNameExtractor(fasta_file=pathOfFasta).list_chromosome_names()
    pathsOfBED = [os.path.join(root, file) for root, dirs, files in os.walk(folderOfBED) for file in files if file != ".gitkeep"]
    num_cores = cpu_count()
    with Pool(processes=num_cores) as pool:
        pool.starmap(process_file, [(bed, fasta_chromosomes, folderOfOutput) for bed in pathsOfBED])


if __name__ == "__main__":
    """
    该脚本用于处理一些文件操作,具体包括对FASTA文件和BED文件夹的操作,并将结果输出到指定的文件夹中。

    参数:
    - pathOfFasta: 字符串类型,表示FASTA文件的路径。
    - folderOfBED: 字符串类型,表示包含BED文件的文件夹路径。
    - folderOfOutput: 字符串类型，表示输出结果的文件夹路径。

    返回值:
    - 无
    """
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="Process some files.")
    # 添加命令行参数
    parser.add_argument("-pf", "--pathOfFasta", type=str, help="设置 FASTA 文件的路径", required=True)
    parser.add_argument("-fbed", "--folderOfBED", type=str, help="设置 BED 文件所在文件夹 (目录) 的路径", default="INPUT/BED")
    parser.add_argument("-fo", "--folderOfOutput", type=str, help="设置输出文件夹 (目录) 的路径", default="OUTPUT")

    # 检查命令行参数数量，若只有一个参数（程序名），则打印帮助信息并退出
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    # 解析命令行参数
    args = parser.parse_args()

    # 调用主函数处理文件
    main(args.pathOfFasta, args.folderOfBED, args.folderOfOutput)
