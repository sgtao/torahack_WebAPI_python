const indexModule = (() => {
  const path = window.location.pathname;
  //
  switch (path) {
    case "/":
      // Usersモジュールのfetchを実行
      return usersModule.fetchAllUsers();
    //
    default:
      break;
  }
})();