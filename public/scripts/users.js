// 即時関数でモジュール化
const usersModule = (() => {
    // const BASE_URL = "http://localhost:3000/api/v1"
    const BASE_ORIGIN = window.location.origin;
    const BASE_PATH = "/api/v1";
    const BASE_URL = BASE_ORIGIN + BASE_PATH;
    //
    // ヘッダーの設定
    const headers = new Headers();
    headers.set("Content-Type", "application/json");
    //
    const handleError = async (res) => {
      const resJson = await res.json();

      switch (res.status) {
        case 200:
          alert(resJson.message);
          window.location.href = "/"; // ホーム画面に戻る
          // window.close(); // 新規作成ウィンドウを閉じる
          break;
        }
    }
    //
    return {
        fetchAllUsers: async () => {
          // await で応答を待ちながら処理する
          const res = await fetch(BASE_URL + '/users');
          const users = await res.json();
          // console.log(res);
          for (let i = 0; i < users.length; i++) {
            const user = users[i];
            const body = `<tr>
                            <td>${user.id}</td>
                            <td>${user.name}</td>
                            <td>${user.profile}</td>
                            <td>${user.date_of_birth}</td>
                            <td>${user.created_at}</td>
                            <td>${user.updated_at}</td>
                            <td>
                            </td>
                          </tr>`;
            document.querySelector('#users-list').insertAdjacentHTML('beforeend', body);
          }
        },
    }
})();