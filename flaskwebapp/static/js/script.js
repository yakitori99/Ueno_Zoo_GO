///// Native javascript
//// 個別ページ
/// escapedページで、ゲットするには[?]クリック時のメッセージ表示
function howToGetClick() {
    // sweetalertを利用する
    swal({
      // type: 'question',
       title: "アニマルをゲットするには"
      ,html: "<div style='text-align:left; margin-top: 1rem;'>" +
            "確信度50%以上でアニマルをゲットできます。<br><br>" +
            "■確信度を上げるには<br>" +
            "画像の認識・分類はAIが自動で行います。<br>" +
            "以下を満たすとうまく認識されやすいので、チャレンジしてみてください。<br>" +
            "・余計なものが写り込まないようにする<br>" +
            "・正面または側面から撮る<br>" +
            "・鮮明に撮る" +
            "<div>"
      ,confirmButtonText: 'OK'
      ,confirmButtonColor: '#00b8d4'
      // ,footer: "<div style='text-align:left; margin:0; padding:0;'>認識できる動物一覧など：<a href='/about'>About</a></div>"
    });
}


/// my_animal_indexページで、選択されたvalueを初期選択する START
function setPulldown_my_animal_index(v){
   var pulldown_option = document.getElementById('user_name_selecter').getElementsByTagName('option');

   for(i=0; i<pulldown_option.length;i++){
     if(pulldown_option[i].value == v){
       pulldown_option[i].selected = true;
       break;
     }
   }
}

document.addEventListener( 'DOMContentLoaded' , function( e ) {
  var selected_user_name_object = document.getElementById('selected_user_name');
  if(selected_user_name_object !== null){
    var selected_user_name = selected_user_name_object.value;
    setPulldown_my_animal_index(selected_user_name);
  }
}, false );
/// my_animal_indexページで、選択されたvalueを初期選択する END


/// photo_library_showページで、選択されたvalueを初期選択する START
function setPulldown_photo_library_show(v){
   var pulldown_option = document.getElementById('animal_no_selecter').getElementsByTagName('option');

   for(i=0; i<pulldown_option.length;i++){
     if(pulldown_option[i].value == v){
       pulldown_option[i].selected = true;
       break;
     }
   }
}

document.addEventListener( 'DOMContentLoaded' , function( e ) {
  var selected_animal_no_object = document.getElementById('selected_animal_no');
  if(selected_animal_no_object !== null){
    var selected_animal_no = selected_animal_no_object.value;
    setPulldown_photo_library_show(selected_animal_no);
  }
}, false );
/// photo_library_showページで、選択されたvalueを初期選択する END


//// jQuery
$(document).ready(function(){
  ///// materialize css の各種機能を有効化
  /// sidenav有効化
  $('.sidenav').sidenav();
  /// リアルタイムで文字数カウントするテキストボックスを有効化
  $('input#input_text, textarea#textarea2').characterCounter();
  /// select(≒ドロップダウンリスト)を有効化
  $('select').formSelect();
  /// modalウインドウ表示を有効化
  $('.modal').modal();


  ///// 自作function
  /// GETボタン押下時
  $("#get_animal_button").on('click', function() {
    var file_list = document.getElementById("get_animal_file").files;
    /// ファイルが取得できない場合はメッセージ表示して処理をキャンセル（空文字の場合など）
    if(file_list.length == 0){
      M.toast({html: 'ファイルを指定してください。', classes: 'grey darken-1'});
      return false;
    }

    /// ファイル拡張子チェックをして、許可していない拡張子の場合はメッセージ表示して処理をキャンセル
    // 許可する拡張子を指定
    var allowed_extensions = ['jpg', 'jpeg', 'png', 'bmp'];
    // 拡張子を取得
    var file_extension = file_list[0].name.split(".").pop().toLowerCase();
    // 拡張子なしをはじくために、split(".")後の長さが1でないことをチェック
    var file_len_after_split = file_list[0].name.split(".").length;
    // チェック実施
    if(allowed_extensions.includes(file_extension) === false  || file_len_after_split == 1){
      M.toast({html: '許可されていないファイル拡張子です。', classes: 'grey darken-1'});
      M.toast({html: 'アップロード可能な拡張子はjpg, jpeg, png, bmpです。', classes: 'grey darken-1'});
      return false;
    }

    /// ファイルサイズチェックをして、10MBを超える場合はメッセージ表示して処理をキャンセル
    if(file_list[0].size > 10485760){
      M.toast({html: '10MB以下のファイルを指定してください。', classes: 'grey darken-1'});
      return false;
    }

    /// GETボタン押下から、classify_img画面への遷移前までの間にプリローダー（ローディング中のアイコン）を表示させる
    $("#get_preloader").css('display', 'inline');
  });

});
