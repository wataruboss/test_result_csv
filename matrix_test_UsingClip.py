import os
import numpy as np
import pandas as pd

########################################################
# 有効数字10桁で末尾0埋めされるように指定
########################################################
np.set_printoptions(precision=10, floatmode='fixed')


########################################################
# ファイルの走査をしてCSVファイルを検出
# ファイル名とファイルパスを取得するclass
########################################################
class get_path:

    def __init__(self, input_directory_path):
        self.input_directory_path = input_directory_path  # inputディレクトリーのパス

    def get_file_path(self):

        file_dict = {}
        for root, directories, files in os.walk(self.input_directory_path):
            for file in files:
                base, ext = os.path.splitext(file)
                file_path = os.path.join(root, file)

                if ext in ['.csv', '.CSV']:
                    file_dict[file] = file_path

        return file_dict


########################################################
# 取得したファイルパスからCSVの読み込み
# ここで計算を行い、Dataframeに変換後ラベルをつけて書き出す
########################################################

class new_csv:  #numpyでファイルを読み書きしてみる
    def __init__(self, file_dict, output_directory_path,rows, specimen):
        self.file_dict = file_dict  # inputディレクトリー内のファイルパスを格納したリスト
        self.output_directory_path = output_directory_path  # outputディレクトリーのパス
        self.rows = rows  # スキップしたい任意のヘッダー行数
        self.specimen = specimen # 試験片寸法

    def output_txt(self):
        for file_name, file_path in self.file_dict.items():
            input_arr = np.loadtxt(file_path, delimiter=",", skiprows=self.rows, encoding='Shift_jis')

            ########################################################
            # 値の計算 clip_guage_average, TrueStress, TrueStrain
            ########################################################
            row, col = np.shape(input_arr)

            Clip_ave = np.reshape(( input_arr[:, 5] + input_arr[:, 6] ) / 2, (row, 1))

            n_stress = np.reshape( input_arr[:, 1] / (self.specimen['b'] * self.specimen['h']), (row, 1))

            n_strain = np.reshape( Clip_ave / self.specimen['l'], (row, 1))

            t_stress = np.reshape( n_stress * (1 + n_strain), (row, 1))

            t_strain = np.reshape( np.log1p(n_strain), (row, 1))

            output_arr = np.hstack((input_arr, Clip_ave, n_stress, n_strain, t_stress, t_strain))

            # ファイル名の変更
            output_file_name = file_name[0:-4]
            output_path = os.path.join(self.output_directory_path, output_file_name + '_output.txt')
            np.savetxt(output_path, output_arr, delimiter="\t", encoding='Shift_jis', fmt='%.8e')


def main():
    print('Enter the Input Directory Path\n')
    input_directory_path = input()  # 元CSVデータが入ってるディレクトリーパスを入力
    print('Enter the Output Directory Path\n')
    output_directory_path = input()  # 出力先ディレクトリーパスの入力
    print('Enter skip rows\n')
    rows = int(input())  # スキップするヘッダー行数を指定

    # 試験片ジオメトリー
    print('Enter specimen geometries')
    print('Enter b=\t')
    b = float(input())
    print('Enter h=\t')
    h = float(input())
    print('enter l=\t')
    l = float(input())
    specimen = {'b': b, 'h': h, 'l': l}


    # get_pathクラスのget_file_path関数を実行
    # ディレクトリー内のCSVを検索、パスとファイル名をそれぞれ別のリストに格納して返ってくる
    directory = get_path(input_directory_path)
    file_dict = directory.get_file_path()

    # new_csvクラスのcut_header関数を実行
    # パスリストを引数に各ファイルについてヘッダー部の削除、outputディレクトリーに名前を変更して保存
    file = new_csv(file_dict, output_directory_path,rows, specimen)
    file.output_txt()


if __name__ == '__main__':
    main()
