const indexModule = (() => {
  const path = window.location.pathname;
  //
  switch (path) {
    case "/":
      // 検索ボタンのイベントを追加
      document.querySelector("#search-btn").addEventListener('click', ()=>{
        return searchModule.searchUsers();
      });
      // Usersモジュールのfetchを実行
      return usersModule.fetchAllUsers();
    //
    case '/create.html' :
      // 保存ボタン・キャンセルボタンのイベントを追加
      document.querySelector("#save-btn").addEventListener('click', ()=>{
        return usersModule.createUser();
      });
      document.querySelector("#cancel-btn").addEventListener('click', ()=>{
        return window.location.href = "/"; // ホーム画面に戻る
        // return window.close(); // 新規作成ウィンドウを閉じる
      });
      break;
    //
    default:
      break;
  }
})();