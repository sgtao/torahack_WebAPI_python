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
    default:
      break;
  }
})();