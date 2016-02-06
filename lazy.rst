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

Optical flowsまたはframeをhdf5 fileに圧縮する
-------------------------------------------







