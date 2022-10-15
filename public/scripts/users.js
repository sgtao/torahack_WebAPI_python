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
      //
      switch (res.status) {
        case 200:
        case 202:
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
                              <a href="edit.html?uid=${user.id}">編集</a>
                            </td>
                          </tr>`;
            document.querySelector('#users-list').insertAdjacentHTML('beforeend', body);
          }
        },
        createUser: async () => {
          const name = document.querySelector("#name").value;
          const profile = document.querySelector("#profile").value;
          const dateOfBirth = document.querySelector("#date-of-birth").value;
          //
          // リクエストのbody
          const body = {
            name: name,
            profile: profile,
            date_of_birth: dateOfBirth
          };
          console.log(body);
          const res = await fetch(BASE_URL + '/users', {
            method: "POST",
            headers: headers,
            body: JSON.stringify(body)
          });
          console.log(res);
          handleError(res);
        },
        setExistingValue: async(uid) => {
          const res = await fetch(BASE_URL + "/user/" + uid);
          const resJson = await res.json();
          //
          document.getElementById('name').value = resJson.name;
          document.getElementById('profile').value = resJson.profile;
          document.getElementById('date-of-birth').value = resJson.date_of_birth;
        },
        saveUser: async (uid) => {
          const name = document.querySelector("#name").value;
          const profile = document.querySelector("#profile").value;
          const dateOfBirth = document.querySelector("#date-of-birth").value;
          // リクエストのbody
          const body = {
            name: name,
            profile: profile,
            date_of_birth: dateOfBirth
          };
          //
          const res = await fetch(BASE_URL + '/user/' + uid, {
            method: "PUT",
            headers: headers,
            body: JSON.stringify(body)
          });
        },
      }
})();