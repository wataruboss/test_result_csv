import pandas as pd
import os


class get_path:

    def __init__(self, input_directory_path):
        self.input_directory_path = input_directory_path  # inputディレクトリーのパス

    # inputディレクトリー内のCSVファイルを探索、ファイルパスとファイル名をそれぞれリストに格納
    def get_file_path(self):

        file_dict = {}
        for root, directories, files in os.walk(self.input_directory_path):
            for file in files:
                base, ext = os.path.splitext(file)
                file_path = os.path.join(root, file)

                if ext in ['.csv', '.CSV']:  # どうも比較演算子はin演算子を使うのが良いみたい。or とか|で区切るとなんかエラー出た。
                    file_dict[file] = file_path

        return file_dict

class new_csv:

    def __init__(self, file_dict, output_directory_path, rows):
        self.file_dict = file_dict  # inputディレクトリー内のファイルパスを格納したリスト
        self.output_directory_path = output_directory_path  # outputディレクトリーのパス
        self.rows = rows  # スキップしたい任意のヘッダー行数

    # 任意の行数のヘッダーを取り除いてoutputディレクトリーにファイルを作成する
    def cut_header(self):

        for file_name, file_path in self.file_dict.items():
            # ファイルを開いてデータフレームを作成
            data_pd = pd.read_csv(file_path, skiprows=self.rows, encoding="Shift_jis")
            # アウトプット用にファイル名を変更
            output_file_name = file_name[0:-4]
            output_path = os.path.join(self.output_directory_path, output_file_name + '_output.txt')

            data_pd.to_csv(output_path, encoding="Shift_jis", index=False)

        return


def main():
    print('Enter the Input Directory Path\n')
    input_directory_path = input()  # 元CSVデータが入ってるディレクトリーパスを入力
    print('Enter the Output Directory Path\n')
    output_directory_path = input()  # 出力先ディレクトリーパスの入力
    print('Enter skip rows\n')
    rows = int(input())  # スキップするヘッダー行数を指定

    # get_pathクラスのget_file_path関数を実行
    # ディレクトリー内のCSVを検索、パスとファイル名をそれぞれ別のリストに格納して返ってくる
    directory = get_path(input_directory_path)
    file_dict = directory.get_file_path()

    # new_csvクラスのcut_header関数を実行
    # パスリストを引数に各ファイルについてヘッダー部の削除、outputディレクトリーに名前を変更して保存
    file = new_csv(file_dict, output_directory_path, rows)
    file.cut_header()


if __name__ == '__main__':
    main()
