# MatchingBED-FA
> [!NOTE]
> 该工具仅适用下载自UCSC的FASTA文件，这里提供下载地址：
> * 人类
>   - [HG38](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz)
> * 小鼠
>   - [MM39](https://hgdownload.soe.ucsc.edu/goldenPath/mm39/bigZips/mm39.fa.gz)

## 环境
### 所需第三方库列表
* Biopython：用于生物信息学数据的处理，包括序列文件的读取与处理。
* pandas：用于数据分析和操作，便于处理结构化数据。
### 第三方库安装步骤
1. 更新pip:
* `python -m pip install --upgrade pip`
2. 安装Biopython:
* `pip install biopython`
3. 安装pandas:
* `pip install pandas`

## 使用方法
* Script文件位于Sources文件夹内
### 参数详解
* -pf, --pathOfFasta：必选参数，用于指定FASTA文件的路径。此参数无默认值，用户必须显式提供。
    * 建议将FASTA参考文件放置于 `INPUT/Ref_FA` 。
* -fbed, --folderOfBED：必选参数，用于指定包含BED文件的文件夹路径。
    * 如果未指定，将使用默认路径 `INPUT/BED` 。
* -fo, --folderOfOutput：可选参数，用于指定输出结果的文件夹路径。
    * 如果未指定，将使用默认路径 `OUTPUT` 。
### 命令格式
* 简便输入
    *    ```python MachingBED_FA.py -pf [pathToYourFasta] -fbed [folderContainingBED] -fo [outputFolder]```
* 完整输入
    *    ```python MachingBED_FA.py --pathOfFasta [pathToYourFasta] --folderOfBED [folderContainingBED] --folderOfOutput [outputFolder]```
### 示例命令
    python MachingBED_FA.py -pf /path/to/your/fastafile.fasta -fbed /path/to/your/bedfolder -fo /path/to/your/outputfolder