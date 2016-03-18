流れ概要は以下のようになる
==========================

1. 動画からOptical flowsとframeを抽出
2. 学習用データ生成
3. 特徴抽出用データ生成

動画からOptical flowsとframeを抽出
---------------------------------

dense_flowをコンパイルする。
研究質の計算のOpenCVはffmpegを追加していないから、別のOpenCVを
利用しなければならない

.. code-block:: html

    # ffmpegをcompile
    # 注意：再コンパイルする時にmake distcleanが必要
    ./configure --prefix=/host/space2/vugia/opencv/ffmpeg-2.8.5_build --enable-shared --enable-pic --enable-static  --disable-yasm
    make; make install;
    # opencvをコンパイル
    # add custom ffmpeg
    # bashの環境変数にcustom ffmpegのpathを追加
    export LD_LIBRARY_PATH=//export/space2/vugia/opencv/ffmpeg-2.8.5_build/lib/
    export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/export/space2/vugia/opencv/ffmpeg-2.8.5_build/lib/pkgconfig
    export PKG_CONFIG_LIBDIR=$PKG_CONFIG_LIBDIR:/export/space2/vugia/opencv/ffmpeg-2.8.5_build//lib/
    # compile opencv with cuda option
    cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/export/space2/vugia/opencv/opencv-2.4.11_build
      -D WITH_CUBLAS=1 ..
    # then compile
    cmake ..; make

コンパイル後 、bash do_extract.sh を実行して、動画からのframeとOptical flowsを抽出する。
抽出されたframeとOptical flowsはJPEGファイルで保存されています。
デフォルト設定を利用すれば、抽出されたファイルは以下のようなファイルで保存する。

.. code-block:: html

    # 動画のサイズを(256x340x3xt)に変更
    # test file
    v_PlayingPiano_g01_c01.avi
    # result
    v_PlayingPiano_g01_c01/
        flow_i_0111.jpg     : 111番目 frame
        flow_x_0123.jpg     : 123番目 Optical flowの水平部
        flow_y_0123.jpg     : 123番目 Optical flowの垂直部


Optical flowsまたはframeをhdf5 fileに圧縮する
-------------------------------------------

LevelDBに圧縮、精度テストなどをしやすくになるため、
一本のショットのOptical flowsまたはframeはhdf5ファイルに圧縮します。
圧縮ルールは以下のようになる。

CaffeのDatum形は[sample_count, data_channels, data_height, data_width]があります。
Opencvのcv2ライブラリは画像を読む時に、画像のデータが[height, width, channel]サイズの
行列に保存されます。
CaffeのDatum形に対応するため、[height, width, channel]から[channel, height, width]
にtransposeすることが必要です。
Optical flowsの場合、画像のchannelは``1''(gray)なので、transposeすることが必要ではありません。

.. code-block:: html

    ### ショットのframe順番（例として15に置く）###
    1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22
    ### T サンプリングを選択（例として3に置く）###
    ## frame_start = 3
    ## frame_end = 20 - 10 - 3 = 7
    3 4 5 6 7
    ## selected frame (選択されたframeの距離は等しい)
    3 5 7
    ## from each selected frame (例として5に置く)
    # frameの場合 #
    5 番目のframe: flow_i_0005.jpg
    # Optical flows: in case of 10 stakced optical flow #
    順番に選択: flow_x_0005.jpg + flow_y_0005.jpg + ... + flow_x_0015.jpg + flow_y_0015.jpg
    サイズ: [20, 256, 340]に圧縮
    ## 選択されたframeまたはOptical flowsの全てをhdf5に圧縮
    # frameの場合 #
    [3, 3 , 256, 340]
    # Optical flowsの場合 #
    [3, 20, 256, 340]

モデルの学習の場合、選択されたframeとOptical flowsの全体を利用します。
学習する時に、caffeの"crop_size"や"mirror"を使えば、
データのrandom croppingとmirroingすることができます。
プログラムは以下のように実行します。

.. code-block:: html

    # Optical flows #
    python merge_OFs.py $DIR $STACKED_COUNT $H5_FILE noncrop $SAMPLING_COUNT;
    # image #
    python merge_imgs.py $DIR $H5_FILE noncrop $SAMPLING_COUNT;


モデルのテストの場合、選択されたframeとOptical flowsの四角と中心部分から[224x224]
サイズを手でcropします。
プログラムは以下のように実行します。

.. code-block:: html

    # image #
    # [3x256x340] -> [3x224x224] x 5
    python merge_imgs.py $DIR $H5_FILE crop 25;
    # Optical flows #
    # [20x256x340] -> [20x224x224] x 20
    python merge_OFs.py $DIR $STACKED_COUNT $H5_FILE crop 25;

Two-stream CNN
----------------

Two-stream CNNの学習用、テスト(validate)用のデータを生成
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

h5list_2lveldb.shを利用して、データを生成します。
学習なので、データのshufflingが必要です。
shufflingのマナーを守るため、h5listは一回shuffleします。
h5list_2lveldb.pyも一回shuffleします。

プログラムは以下のように実行します。

.. code-block:: html

    bash h5list_2leveldb.sh

学習
^^^^^^^^

学習前に、データのmeanファイルを生成します。

.. code-block:: html

    caffe/build/tool/compute_mean.bin -backend leveldb leveldb_path output_mean_file

meanファイルを生成あと、two-stream_learnの中にあるscriptを利用して、学習を行います。
batch=256は大きいので、より小さい値を利用する場合、学習step数を増えなければなりません。

プログラムは以下のように実行します。

.. code-block:: html

    bash train_temporal.sh train_temporal.conf

テスト
^^^^^^^^^^^

上記に記載されたことを通じて、テストを生成します。
テストサイズは[125x3x224x224], [125x10x224x224],...です。
プログラムは以下のように実行します。

.. code-block:: html

    Usage python test_network.py network(_cls.txt) trained_model mean_file test_h5_list


テストの精度を上れるため、テストデータの"mirror"も使わなければなりません。
テストサイズは[250x3x224x224], [250x10x224x224],...になります。

.. code-block:: html

    input_dim: 125      -> 250 になる

特徴抽出
^^^^^^^^^

extract_featuresの中にあるファイルを利用する。

.. code-block:: html

    "Usage python %s network trained_model mean_file h5_list features_directory
    "Usage python %s network trained_model mean_file imgs_list features_file"

Siameseネット
------------

学習
^^^^^

特徴抽出
^^^^^^^^

